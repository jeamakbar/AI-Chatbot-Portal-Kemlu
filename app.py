# --- LIBRARIES & EXTERNAL MODULES ---
import os
import re
import logging
import requests
import time
from datetime import datetime
from flask import Flask, render_template, request, jsonify
from urllib.parse import quote_plus
import firebase_admin
from firebase_admin import credentials, firestore
from collections import OrderedDict

# --- INTERNAL MODULES & CONSTANTS ---
from constants import (
    ADDRESS_KEYWORDS_PATTERN, GREETING_PATTERN, LOST_DOCUMENT_PATTERN,
    KEYWORDS_EN, KEYWORDS_ID, GENERIC_FOLLOW_UPS, GREETINGS,
    STATIC_FALLBACKS, GENERIC_FALLBACK,
    LLM_API_URL, LLM_SYSTEM_PROMPTS, LLM_FOLLOW_UP_INSTRUCTIONS,
    RESPONSE_SEPARATOR, MAX_CONVERSATION_HISTORY, PERWAKILAN_DATA
)
from location_utils import find_location_info, get_all_cities

# --- APP SETUP & CONFIGURATION ---
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

# === FIREBASE INITIALIZATION ===
try:
    cred = credentials.Certificate("firebase-service-account.json")
    firebase_admin.initialize_app(cred)
    db = firestore.client()
    logging.info("Firebase Firestore connection initialized successfully.")
except Exception as e:
    db = None
    logging.error(f"Failed to initialize Firebase: {e}. Firestore logging will be disabled.")

app = Flask(__name__, template_folder='views', static_folder='static')

# --- CACHE & SESSION MANAGEMENT ---
MAX_CACHE_SIZE = 100
CACHE_TTL_SECONDS = 3600  # Cache is valid for 1 hour
llm_cache = OrderedDict()

app.config['LLM_API_KEY'] = os.environ.get("LLM_API_KEY", "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")
app.config['LLM_MODEL'] = os.environ.get("LLM_MODEL", "deepseek/deepseek-chat")
app.config['LLM_TIMEOUT'] = int(os.environ.get("LLM_TIMEOUT", 30))

conversation_histories = {}
session_contexts = {} # Stores the last topic for each session
session_triggered_keywords = {}


# --- HELPER FUNCTIONS ---
def log_activity(session_id, user_input, bot_response, response_type, lang):
    """Logs interaction activity to Firestore."""
    if not db:
        logging.warning("Firestore client not available. Skipping audit log.")
        return
    try:
        log_ref = db.collection('audit_logs').document()
        log_ref.set({
            'timestamp': datetime.now(),
            'session_id': session_id,
            'language': lang,
            'user_input': user_input,
            'bot_response': bot_response,
            'response_type': response_type
        })
    except Exception as e:
        logging.error(f"Failed to write to Firestore audit log: {e}")

def convert_markdown_to_html(text: str) -> str:
    """Converts simple Markdown to HTML."""
    if not isinstance(text, str): return text
    text = re.sub(r'\*\*(.*?)\*\*', r'<strong>\1</strong>', text)
    text = re.sub(r'\[(.*?)\]\((.*?)\)', r'<a href="\2" target="_blank">\1</a>', text)
    return text

def get_accurate_maps_url(address: str) -> str:
    """Generates a functional Google Maps search URL."""
    base_url = "https://www.google.com/maps/search/?api=1&query="
    encoded_address = quote_plus(address)
    maps_url = base_url + encoded_address
    logging.info(f"Generated Google Maps URL: {maps_url}")
    return maps_url

def get_local_data_context(lang: str = "id") -> str:
    """Builds a context string from local data for the LLM."""
    context = "## Konteks Informasi Lokal yang Tersedia\n" if lang == "id" else "## Available Local Information Context\n"
    context += "Anda memiliki akses ke data internal berikut. Gunakan informasi ini untuk memberikan jawaban yang lebih akurat.\n\n" if lang == "id" else "You have access to the following internal data. Use this information to provide more accurate answers.\n\n"
    
    keywords_list = KEYWORDS_ID if lang == "id" else KEYWORDS_EN
    context += "### Daftar Layanan Umum dan Kata Kunci Terkait:\n" if lang == "id" else "### List of General Services and Related Keywords:\n"
    for item in keywords_list:
        main_keyword = item['pattern'].replace('\\', '').replace('(', '').replace(')', '').split('|')[0].strip()
        if main_keyword:
            context += f"- **{main_keyword.title()}**: Terkait dengan {item.get('context', 'informasi layanan ' + main_keyword)}.\n" if lang == "id" else f"- **{main_keyword.title()}**: Related to {item.get('context', 'service information for ' + main_keyword)}.\n"
    
    context += "\n### Daftar Perwakilan RI (KBRI/KJRI) yang Datanya Tersedia:\n" if lang == "id" else "\n### List of Available Indonesian Missions (Embassies/Consulates):\n"
    all_locations = [details['name'] for continent in PERWAKILAN_DATA.values() for details in continent.values()]
    context += ", ".join(sorted(all_locations)) + ".\n"
    context += "Jika pengguna menanyakan alamat dari salah satu perwakilan ini, Anda dapat merujuk ke informasi tersebut.\n" if lang == "id" else "If the user asks for the address of one of these missions, you can refer to this information.\n"
    return context

def get_llm_response(messages: list, lang: str = "id", context: str = "") -> tuple[str | None, list]:
    """Gets a response from the LLM API."""
    api_key = app.config.get('LLM_API_KEY')
    if not api_key or "GANTI_DENGAN_API_KEY_ANDA" in api_key:
        logging.error("LLM_API_KEY is not set. Skipping LLM call.")
        return None, []

    local_context = get_local_data_context(lang)
    system_content = (f"{LLM_SYSTEM_PROMPTS.get(lang, LLM_SYSTEM_PROMPTS['id'])}\n\n{local_context}\n\n{context}\n\n{LLM_FOLLOW_UP_INSTRUCTIONS.get(lang, LLM_FOLLOW_UP_INSTRUCTIONS['id'])}")
    system_prompt = [{"role": "system", "content": system_content}]
    headers = {"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"}
    payload = {"model": app.config.get('LLM_MODEL'), "messages": system_prompt + messages, "max_tokens": 1536, "temperature": 0.2}

    max_retries = 3
    base_delay = 1
    for attempt in range(max_retries):
        try:
            response = requests.post(LLM_API_URL, json=payload, headers=headers, timeout=app.config.get('LLM_TIMEOUT'))
            if response.status_code == 429:
                delay = base_delay * (2 ** attempt)
                logging.warning(f"Rate limit exceeded (429). Retrying in {delay}s...")
                time.sleep(delay)
                continue
            response.raise_for_status()
            data = response.json()
            full_content = data.get("choices", [{}])[0].get("message", {}).get("content", "").strip()
            if RESPONSE_SEPARATOR in full_content:
                main_answer, follow_up_raw = full_content.split(RESPONSE_SEPARATOR, 1)
                follow_ups = [q.strip() for q in follow_up_raw.split('|') if q.strip().endswith('?')]
                return main_answer.strip(), follow_ups[:3]
            return full_content, []
        except requests.exceptions.RequestException as e:
            logging.error(f"LLM API call failed on attempt {attempt + 1}: {e}")
            if hasattr(e, 'response') and e.response is not None:
                logging.error(f"LLM API Response Status: {e.response.status_code}")
                logging.error(f"LLM API Response Body: {e.response.text}")
            if attempt < max_retries - 1:
                time.sleep(base_delay * (2 ** attempt))
            else:
                return None, []
    return None, []

def get_contextual_link(user_input: str, lang: str = "id") -> str:
    """Adds a relevant link based on user input."""
    user_input_lower = user_input.lower()
    if any(keyword in user_input_lower for keyword in ["paspor", "visa", "legalisasi", "konsuler", "passport", "legalization"]):
        return ('<br><br>Untuk informasi resmi mengenai layanan konsuler, kunjungi <a href="https://kemlu.go.id/layanan/layanan-konsuler-fasilitas-diplomatik-dan-pelindungan-wni/kekonsuleran" target="_blank">halaman Kekonsuleran Kemlu</a>.' if lang == 'id' else '<br><br>For official information on consular services, visit the <a href="https://kemlu.go.id/layanan/layanan-konsuler-fasilitas-diplomatik-dan-pelindungan-wni/kekonsuleran" target="_blank">Ministry\'s Consular Affairs page</a>.')
    if any(keyword in user_input_lower for keyword in ["lapor diri", "pelindungan", "bantuan wni", "darurat", "emergency", "protection"]):
        return ('<br><br>Untuk lapor diri dan informasi pelindungan WNI, kunjungi <a href="https://peduliwni.kemlu.go.id/" target="_blank">portal Peduli WNI</a>.' if lang == 'id' else '<br><br>For self-registration and citizen protection, visit the <a href="https://peduliwni.kemlu.go.id/" target="_blank">Peduli WNI portal</a>.')
    if any(keyword in user_input_lower for keyword in ["kbri", "kjri", "kedutaan", "konsulat", "embassy", "consulate", "perwakilan"]):
        return ('<br><br>Daftar lengkap Perwakilan RI dapat ditemukan di <a href="https://kemlu.go.id/perwakilan" target="_blank">halaman Perwakilan Kemlu</a>.' if lang == 'id' else '<br><br>The complete list of Indonesian Missions can be found on the <a href="https://kemlu.go.id/perwakilan" target="_blank">Ministry\'s Missions page</a>.')
    return ""

def get_static_fallback(user_input_lower: str, lang: str) -> tuple[str, str] | None:
    """Provides a helpful static response if the LLM fails."""
    fallbacks = STATIC_FALLBACKS.get(lang, {})
    for pattern, answer in fallbacks.items():
        if re.search(pattern, user_input_lower):
            logging.warning(f"LLM failed, providing static fallback for pattern: {pattern}")
            return answer, "static_fallback"
    return None, None

# --- CORE MESSAGE PROCESSING LOGIC ---
def handle_lost_document(user_input_lower: str, lang: str) -> tuple[str, list, str] | None:
    """Handles requests about lost documents."""
    if not re.search(LOST_DOCUMENT_PATTERN, user_input_lower):
        return None
    
    location_match = re.search(r"(di|in)\s+([\w\s]+)", user_input_lower)
    location_name = ""
    if location_match:
        location_name = location_match.group(2).strip()

    info, score = (find_location_info(location_name) if location_name else (None, 0))

    if info and score > 80:
        maps_link = get_accurate_maps_url(info['address'])
        context = info['name']
        if lang == "en":
            reply_text = (f"<strong>Guidance for Lost Passport in {info['name'].split(' ')[-1]}</strong><br>You should immediately contact the <b>{info['name']}</b> for assistance.<br><br><strong>Contact Details:</strong><ul><li><b>Address:</b> {info['address']} <a href='{maps_link}' target='_blank'>(View on Map)</a></li><li><b>Website:</b> <a href='{info['link']}' target='_blank'>{info['link']}</a></li></ul>")
            follow_ups = ["What are the requirements for an Emergency Travel Document?", "How much does it cost?", "What are the opening hours?"]
        else:
            reply_text = (f"<strong>Panduan Kehilangan Paspor di {info['name'].split(' ')[-1]}</strong><br>Anda harus segera menghubungi <b>{info['name']}</b> untuk mendapatkan bantuan.<br><br><strong>Detail Kontak:</strong><ul><li><b>Alamat:</b> {info['address']} <a href='{maps_link}' target='_blank'>(Lihat di Peta)</a></li><li><b>Situs Web:</b> <a href='{info['link']}' target='_blank'>{info['link']}</a></li></ul>")
            follow_ups = ["Apa saja syarat mengurus SPLP?", "Berapa biayanya?", "Apa saja jam bukanya?"]
        return reply_text, follow_ups, context

    default_reply = ("Saya memahami Anda kehilangan dokumen. Mohon informasikan di kota dan negara mana Anda berada agar saya dapat membantu lebih lanjut.", ["Saya kehilangan paspor di Berlin", "Dokumen saya hilang di Singapura"]) if lang == "id" else ("I understand you've lost a document. To help, please tell me which city and country you are in.", ["I lost my passport in Berlin", "My document is missing in Singapore"])
    return default_reply[0], default_reply[1], "dokumen hilang"


def handle_address_request(user_input_lower: str, lang: str) -> tuple[str, list, str] | None:
    """Handles requests for representative addresses."""
    address_match = re.search(ADDRESS_KEYWORDS_PATTERN, user_input_lower, re.IGNORECASE)
    if not address_match:
        return None
        
    location_name = address_match.groups()[-1].strip()
    info, score = find_location_info(location_name)
    
    if info and score > 80: # Using a threshold for fuzzy match
        maps_link = get_accurate_maps_url(info['address'])
        context = info['name']
        if lang == "en":
            reply_text = (f"<strong>Information for {info['name']}</strong><ul><li><b>Address:</b> {info['address']}</li><li><b>Map:</b> <a href='{maps_link}' target='_blank'>View on Google Maps</a></li><li><b>Website:</b> <a href='{info['link']}' target='_blank'>{info['link']}</a></li></ul>")
            follow_ups = ["What are the consular service hours?", "Do I need an appointment?"]
        else:
            reply_text = (f"<strong>Informasi untuk {info['name']}</strong><ul><li><b>Alamat:</b> {info['address']}</li><li><b>Peta:</b> <a href='{maps_link}' target='_blank'>Lihat di Google Maps</a></li><li><b>Situs Web:</b> <a href='{info['link']}' target='_blank'>{info['link']}</a></li></ul>")
            follow_ups = ["Apa saja jam layanan konsuler?", "Apakah saya perlu membuat janji temu?"]
        return reply_text, follow_ups, context
    return None

def process_user_message(user_input: str, lang: str, session_id: str) -> tuple[str | None, list, str, str | None]:
    """Processes the user's message and determines the appropriate response."""
    user_input_lower = user_input.lower()
    
    # 1. Greeting Intent
    if re.search(GREETING_PATTERN, user_input_lower):
        return GREETINGS.get(lang), GENERIC_FOLLOW_UPS.get(lang, []), "greeting", None

    # 2. Address Request Intent
    response = handle_address_request(user_input_lower, lang)
    if response:
        return response[0], response[1], "address_request", response[2]

    # 3. Lost Document Intent
    response = handle_lost_document(user_input_lower, lang)
    if response:
        return response[0], response[1], "lost_document", response[2]

    # 4. General Keyword Intent
    keywords_list = sorted(KEYWORDS_ID if lang == "id" else KEYWORDS_EN, key=lambda x: x['priority'], reverse=True)
    for item in keywords_list:
        if re.search(item['pattern'], user_input_lower):
            session_triggered_keywords.setdefault(session_id, set()).add(item['pattern'])
            return item["answer"], item["follow_up"], "keyword_match", item.get("context")
            
    # 5. Fallback to LLM
    return None, [], "llm_fallback", None


# --- FLASK ROUTES (API ENDPOINTS) ---
@app.route("/")
def index():
    """Renders the main chatbot page."""
    return render_template("index.html")

@app.route("/ask", methods=["POST"])
def ask():
    """Main endpoint to receive and respond to chatbot messages."""
    data = request.get_json()
    if not data: return jsonify({"error": "Invalid JSON"}), 400
    
    user_input_original = data.get("message", "").strip()
    user_input = user_input_original
    lang = data.get("language", "id")
    session_id = data.get("session_id")

    if not session_id: return jsonify({"reply": "Error: session_id is missing.", "follow_up": []}), 400
    
    # Context Enrichment for follow-up questions
    last_context = session_contexts.get(session_id)
    if last_context and len(user_input.split()) <= 5:
        # Check if the user is asking a generic question that needs context
        follow_up_keywords = ["syarat", "biaya", "prosedur", "dokumen", "langkah", "jam buka", 
                              "requirements", "cost", "procedure", "documents", "steps", "opening hours"]
        if any(keyword in user_input.lower() for keyword in follow_up_keywords):
            contextual_input = f"Terkait {last_context}, {user_input}" if lang == "id" else f"Regarding {last_context}, {user_input}"
            logging.info(f"Short query with context. Transforming '{user_input}' to '{contextual_input}'")
            user_input = contextual_input
    
    history = conversation_histories.setdefault(session_id, [])
    if len(history) > MAX_CONVERSATION_HISTORY * 2: history = history[-(MAX_CONVERSATION_HISTORY * 2):]
    
    reply_text, follow_up_questions, response_type, context = process_user_message(user_input, lang, session_id)
    
    # Save new context if available
    if context:
        session_contexts[session_id] = context
    
    if not reply_text:
        response_type = 'llm'
        cache_key = f"{lang}:{user_input.lower()}"
        
        # Check cache
        if cache_key in llm_cache and (datetime.now() - llm_cache[cache_key][1]).total_seconds() < CACHE_TTL_SECONDS:
            logging.info(f"Serving response from valid cache for key: {cache_key}")
            llm_answer, llm_follow_ups = llm_cache[cache_key][0]
            llm_cache.move_to_end(cache_key)
        else:
            if cache_key in llm_cache:
                logging.info(f"Cache expired for key: {cache_key}. Removing.")
                del llm_cache[cache_key]

            logging.info(f"Cache miss or expired for key: {cache_key}. Calling LLM API.")
            context_summary = f"User has previously asked about: {', '.join(session_triggered_keywords.get(session_id, []))}"
            # Add last context to LLM prompt
            llm_context_prompt = f"Current conversation context is about: {last_context}." if last_context else ""
            
            llm_answer, llm_follow_ups = get_llm_response(history + [{"role": "user", "content": user_input}], lang, context=f"{context_summary}\n{llm_context_prompt}")

            if llm_answer:
                llm_cache[cache_key] = ((llm_answer, llm_follow_ups), datetime.now())
                if len(llm_cache) > MAX_CACHE_SIZE:
                    llm_cache.popitem(last=False)

        if llm_answer:
            reply_text = convert_markdown_to_html(llm_answer)
            link_addition = get_contextual_link(user_input, lang)
            if link_addition and "kemlu.go.id" not in reply_text:
                 reply_text += link_addition
            follow_up_questions = llm_follow_ups
            # Clear context after a successful LLM response that seems to resolve the follow-up
            session_contexts.pop(session_id, None)
        else:
            # Tiered Fallback Logic
            logging.error("LLM call failed after retries. Attempting static fallback.")
            reply_text, response_type = get_static_fallback(user_input.lower(), lang)
            
            if not reply_text:
                logging.error("No static fallback found. Using generic fallback.")
                reply_text = GENERIC_FALLBACK.get(lang)
                response_type = "generic_fallback"
            
            follow_up_questions = GENERIC_FOLLOW_UPS.get(lang, [])
    
    history.append({"role": "user", "content": user_input_original})
    history.append({"role": "assistant", "content": reply_text})
    conversation_histories[session_id] = history
    
    log_activity(session_id, user_input_original, reply_text, response_type, lang)
    
    return jsonify({"reply": reply_text, "follow_up": follow_up_questions})

@app.route('/report', methods=['POST'])
def report():
    """Receives feedback/reports from users and saves them to Firestore."""
    if not db: return jsonify({'status': 'error', 'message': 'Database not configured'}), 500
    data = request.get_json()
    if not data or 'feedback' not in data or 'session_id' not in data:
        return jsonify({'status': 'error', 'message': 'Invalid data'}), 400
    try:
        feedback_ref = db.collection('feedback').document()
        feedback_ref.set({'timestamp': datetime.now(), 'session_id': data['session_id'], 'feedback_text': data['feedback']})
        return jsonify({'status': 'success', 'message': 'Feedback received'})
    except Exception as e:
        logging.error(f"Failed to write feedback to Firestore: {e}")
        return jsonify({'status': 'error', 'message': 'Could not save feedback'}), 500

@app.route('/feedback', methods=['POST'])
def feedback():
    """Receives ratings (thumbs up/down) from users."""
    if not db: return jsonify({'status': 'error', 'message': 'Database not configured'}), 500
    data = request.get_json()
    if not data or 'vote' not in data or 'session_id' not in data or 'message' not in data:
        return jsonify({'status': 'error', 'message': 'Invalid data'}), 400
    try:
        feedback_ref = db.collection('review').document()
        feedback_ref.set({'timestamp': datetime.now(), 'session_id': data['session_id'], 'vote': data['vote'], 'message': data['message']})
        return jsonify({'status': 'success', 'message': 'Feedback received'})
    except Exception as e:
        logging.error(f"Failed to write review to Firestore: {e}")
        return jsonify({'status': 'error', 'message': 'Could not save feedback'}), 500

# --- APPLICATION ENTRY POINT ---
if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)