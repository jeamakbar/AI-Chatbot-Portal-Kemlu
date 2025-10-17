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
from dotenv import load_dotenv

# --- scikit-learn Integration ---
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# --- KNOWLEDGE BASE SETUP FOR RAG ---
from constants import KEYWORDS_ID # Import KEYWORDS_ID for RAG
# Siapkan data dari constants.py sebagai knowledge base
knowledge_base = [item for item in KEYWORDS_ID if 'answer' in item and 'pattern' in item]
# Gunakan 'pattern' sebagai dokumen yang akan di-vectorize
rag_documents = [item['pattern'] for item in knowledge_base]

# Inisialisasi TF-IDF Vectorizer
# Ini akan mengubah teks menjadi representasi angka (vektor)
vectorizer = TfidfVectorizer()
tfidf_matrix = vectorizer.fit_transform(rag_documents)

# --- INTERNAL MODULES & CONSTANTS ---
from constants import (
    ADDRESS_KEYWORDS_PATTERN, GREETING_PATTERN, LOST_DOCUMENT_PATTERN,
    KEYWORDS_EN, GENERIC_FOLLOW_UPS, GREETINGS,
    STATIC_FALLBACKS, GENERIC_FALLBACK,
    LLM_SYSTEM_PROMPTS, LLM_FOLLOW_UP_INSTRUCTIONS,
    RESPONSE_SEPARATOR, MAX_CONVERSATION_HISTORY, PERWAKILAN_DATA
)
from location_utils import find_location_info, get_all_cities

# Load environment variables from .env file
load_dotenv()

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

# --- CACHE, SESSION & LINK MAP MANAGEMENT ---
MAX_CACHE_SIZE = 100
CACHE_TTL_SECONDS = 3600
llm_cache = OrderedDict()
LINK_MAP = {}

# --- SUMBER DATA TAUTAN UTAMA ---
MASTER_LINK_MAP = {
    # Kebijakan / Policy
    "asean": "https://kemlu.go.id/kebijakan/asean",
    "diplomasi ekonomi": "https://kemlu.go.id/kebijakan/diplomasi-ekonomi",
    "economic diplomacy": "https://kemlu.go.id/kebijakan/diplomasi-ekonomi",
    "isu khusus": "https://kemlu.go.id/kebijakan/isu-khusus",
    "special issues": "https://kemlu.go.id/kebijakan/isu-khusus",
    "kerja sama bilateral": "https://kemlu.go.id/kebijakan/kerja-sama-bilateral",
    "bilateral cooperation": "https://kemlu.go.id/kebijakan/kerja-sama-bilateral",
    "kerja sama multilateral": "https://kemlu.go.id/kebijakan/kerja-sama-multilateral",
    "multilateral cooperation": "https://kemlu.go.id/kebijakan/kerja-sama-multilateral",
    "kerja sama regional": "https://kemlu.go.id/kebijakan/kerja-sama-regional",
    "regional cooperation": "https://kemlu.go.id/kebijakan/kerja-sama-regional",
    "landasan visi dan misi polugri": "https://kemlu.go.id/kebijakan/landasan-visi-dan-misi-polugri",
    "vision and mission of foreign policy": "https://kemlu.go.id/kebijakan/landasan-visi-dan-misi-polugri",
    "organisasi internasional": "https://kemlu.go.id/kebijakan/organisasi-internasional",
    "international organizations": "https://kemlu.go.id/kebijakan/organisasi-internasional",
    "pengarusutamaan gender": "https://kemlu.go.id/kebijakan/pengarusutamaan-gender",
    "gender mainstreaming": "https://kemlu.go.id/kebijakan/pengarusutamaan-gender",
    "reformasi birokrasi kemlu": "https://kemlu.go.id/kebijakan/reformasi-birokrasi-kemlu",
    "bureaucratic reform": "https://kemlu.go.id/kebijakan/reformasi-birokrasi-kemlu",

    # Kinerja / Performance
    "kinerja kementerian luar negeri": "https://kemlu.go.id/kinerja/kinerja-kementerian-luar-negeri",
    "ministry performance": "https://kemlu.go.id/kinerja/kinerja-kementerian-luar-negeri",

    # Publikasi / Publications
    "agenda": "https://kemlu.go.id/publikasi/agenda",
    "events": "https://kemlu.go.id/publikasi/agenda",
    "buku diplomasi ekonomi kreatif": "https://kemlu.go.id/publikasi/buku/buku-diplomasi-ekonomi-kreatif",
    "creative economy diplomacy book": "https://kemlu.go.id/publikasi/buku/buku-diplomasi-ekonomi-kreatif",
    "buku diplomasi indonesia": "https://kemlu.go.id/publikasi/buku/buku-diplomasi-indonesia",
    "indonesian diplomacy book": "https://kemlu.go.id/publikasi/buku/buku-diplomasi-indonesia",
    "galeri diplomasi": "https://kemlu.go.id/publikasi/galeri-diplomasi",
    "diplomacy gallery": "https://kemlu.go.id/publikasi/galeri-diplomasi",
    "jurnal hubungan luar negeri": "https://kemlu.go.id/publikasi/jurnal/jurnal-hubungan-luar-negeri",
    "foreign affairs journal": "https://kemlu.go.id/publikasi/jurnal/jurnal-hubungan-luar-negeri",
    "opinio juris": "https://kemlu.go.id/publikasi/jurnal/opinio-juris",
    "treaty journal": "https://kemlu.go.id/publikasi/jurnal/treaty-journal",
    "policy brief": "https://kemlu.go.id/publikasi/kajian/policy-brief-",
    "majalah": "https://kemlu.go.id/publikasi/majalah",
    "magazine": "https://kemlu.go.id/publikasi/majalah",
    "pidato presiden": "https://kemlu.go.id/publikasi/pidato/pidato-presiden",
    "president speech": "https://kemlu.go.id/publikasi/pidato/pidato-presiden",
    "pidato menteri": "https://kemlu.go.id/publikasi/pidato/pidato-menteri",
    "minister speech": "https://kemlu.go.id/publikasi/pidato/pidato-menteri",
    "pidato lainnya": "https://kemlu.go.id/publikasi/pidato/pidato-lainnya",
    "other speeches": "https://kemlu.go.id/publikasi/pidato/pidato-lainnya",
    "siaran pers": "https://kemlu.go.id/publikasi/siaran-pers",
    "press release": "https://kemlu.go.id/publikasi/siaran-pers",
    "tabloid diplomasi": "https://kemlu.go.id/publikasi/tabloid-diplomasi",
    "diplomacy tabloid": "https://kemlu.go.id/publikasi/tabloid-diplomasi",

    # Info & Layanan Umum / General Info & Services
    "ppid": "https://kemlu.go.id/ppid",
    "public information": "https://kemlu.go.id/ppid",
    "berita": "https://kemlu.go.id/berita",
    "news": "https://kemlu.go.id/berita",
    "daftar joint statement": "https://kemlu.go.id/daftar-joint-statement",
    "joint statements": "https://kemlu.go.id/daftar-joint-statement",
    "gedung pancasila": "https://kemlu.go.id/tentang-kami/bangunan-bersejarah/gedung-pancasila-",
    "pancasila building": "https://kemlu.go.id/tentang-kami/bangunan-bersejarah/gedung-pancasila-",
    "museum konferensi asia afrika": "https://kemlu.go.id/tentang-kami/bangunan-bersejarah/museum-konferensi-asia-afrika-",
    "asian african conference museum": "https://kemlu.go.id/tentang-kami/bangunan-bersejarah/museum-konferensi-asia-afrika-",
    "struktur organisasi": "https://kemlu.go.id/tentang-kami/struktur-organisasi",
    "organizational structure": "https://kemlu.go.id/tentang-kami/struktur-organisasi",
    "jaringan dokumentasi dan informasi hukum": "https://kemlu.go.id/layanan/jaringan-dokumentasi-dan-informasi-hukum",
    "legal documentation network": "https://kemlu.go.id/layanan/jaringan-dokumentasi-dan-informasi-hukum",
    "kartu masyarakat indonesia di luar negeri": "https://kemlu.go.id/layanan/kartu-masyarakat-indonesia-di-luar-negeri",
    "indonesian diaspora card": "https://kemlu.go.id/layanan/kartu-masyarakat-indonesia-di-luar-negeri",
    "daftar perwakilan diplomatik dan konsuler asing": "https://kemlu.go.id/layanan/layanan-konsuler-fasilitas-diplomatik-dan-pelindungan-wni/daftar-perwakilan-diplomatik-dan-konsuler-asing",
    "foreign diplomatic missions": "https://kemlu.go.id/layanan/layanan-konsuler-fasilitas-diplomatik-dan-pelindungan-wni/daftar-perwakilan-diplomatik-dan-konsuler-asing",
    "fasilitas diplomatik": "https://kemlu.go.id/layanan/layanan-konsuler-fasilitas-diplomatik-dan-pelindungan-wni/fasilitas-diplomatik",
    "diplomatic facilities": "https://kemlu.go.id/layanan/layanan-konsuler-fasilitas-diplomatik-dan-pelindungan-wni/fasilitas-diplomatik",
    "pendaftaran ormas asing indonesia": "https://kemlu.go.id/layanan/pendaftaran-ormas-asing-indonesia",
    "foreign ngo registration": "https://kemlu.go.id/layanan/pendaftaran-ormas-asing-indonesia",
    "pengaduan masyarakat": "https://kemlu.go.id/layanan/pengaduan-masyarakat",
    "public complaints": "https://kemlu.go.id/layanan/pengaduan-masyarakat",
    "pelayanan media": "https://kemlu.go.id/layanan/pelayanan-media",
    "media services": "https://kemlu.go.id/layanan/pelayanan-media",
    "rogatory online": "https://kemlu.go.id/layanan/rogatory-online",
    "treaty database": "https://kemlu.go.id/layanan/treaty-database",
    "unit kerja pengadaan barang/jasa|ukpbj": "https://kemlu.go.id/layanan/unit-kerja-pengadaan-barangjasa-ukpbj",
    "procurement services unit": "https://kemlu.go.id/layanan/unit-kerja-pengadaan-barangjasa-ukpbj",
    "perwakilan": "https://kemlu.go.id/perwakilan",
    "missions": "https://kemlu.go.id/perwakilan",
    "perwakilan ri": "https://kemlu.go.id/perwakilan",
    "karir": "https://kemlu.go.id/karir",
    "career": "https://kemlu.go.id/karir",
    "kontak": "https://kemlu.go.id/kontak",
    "contact": "https://kemlu.go.id/kontak",
    "faq": "https://kemlu.go.id/faq",
    "peta situs": "https://kemlu.go.id/peta-situs",
    "sitemap": "https://kemlu.go.id/peta-situs",
    "tautan": "https://kemlu.go.id/tautan",
    "links": "https://kemlu.go.id/tautan",

    # Layanan Pelindungan WNI
    "portal peduli wni|peduli wni": "https://peduliwni.kemlu.go.id/",
    "citizen protection portal|peduli wni": "https://peduliwni.kemlu.go.id/",
    "lapor diri": "https://kemlu.go.id/etc/lapor-diri-online",
    "self report": "https://kemlu.go.id/etc/lapor-diri-online",
    "safe travel": "https://kemlu.go.id/pelindungan-wni-di-luar-negeri/safe-travel",
    "pemberian fasilitas pelindungan wni": "https://kemlu.go.id/etc/pemberian-fasilitasi-pelindungan-wni",
    "providing facilitation for the protection of indonesia citizens": "https://kemlu.go.id/etc/pemberian-fasilitasi-pelindungan-wni",
    "kampanye penyadaran publik": "https://kemlu.go.id/etc/kampanye-penyadaran-publik",
    "public awareness campaign": "https://kemlu.go.id/etc/kampanye-penyadaran-publik",
    "penerimaan permohonan pelindungan wni di luar negeri": "https://kemlu.go.id/etc/penerimaan-permohonan-pelindungan-wni-di-luar-negeri",
    "acceptance of applications for protection of indonesian citizens abroad": "https://kemlu.go.id/etc/penerimaan-permohonan-pelindungan-wni-di-luar-negeri",
    
    # Layanan Konsuler, Fasilitas Diplomatik, & Legalisasi (Consular, Diplomatic Facility, & Legalization Services)
    "layanan konsuler": "https://kemlu.go.id/layanan/layanan-konsuler-fasilitas-diplomatik-dan-pelindungan-wni/kekonsuleran",
    "consular services": "https://kemlu.go.id/layanan/layanan-konsuler-fasilitas-diplomatik-dan-pelindungan-wni/kekonsuleran",
    "legalisasi dokumen": "https://kemlu.go.id/etc/legalisasi-dokumen",
    "layanan legalisasi dokumen": "https://kemlu.go.id/etc/legalisasi-dokumen",
    "document legalization": "https://kemlu.go.id/etc/legalisasi-dokumen",
    "visa|visa indonesia": "https://kemlu.go.id/etc/informasi-kebijakan-visa-republik-indonesia",
    "indonesia visa": "https://kemlu.go.id/etc/informasi-kebijakan-visa-republik-indonesia",
    "paspor|paspor diplomatik|paspor dinas": "https://kemlu.go.id/etc/pelayanan-paspor-diplomatik-dan-dinas",
    "diplomatic passport|passport": "https://kemlu.go.id/etc/pelayanan-paspor-diplomatik-dan-dinas",
    "exit permit only": "https://kemlu.go.id/etc/exit-permit-only",
    "izin tinggal|izin tinggal diplomatik": "https://kemlu.go.id/etc/izin-tinggal-diplomatik-dan-dinas",
    "diplomatic and service stay permit": "https://kemlu.go.id/etc/izin-tinggal-diplomatik-dan-dinas",
    "izin penerbangan": "https://kemlu.go.id/etc/izin-penerbangan",
    "flight permit": "izin-penerbangan",
    "izin perkapalan": "https://kemlu.go.id/etc/izin-perkapalan",
    "shipping permit": "https://kemlu.go.id/etc/izin-perkapalan",
    "jasa konsuler bagi wna": "https://kemlu.go.id/etc/jasa-konsuler-bagi-wna",
    "consular services for foreigners": "https://kemlu.go.id/etc/jasa-konsuler-bagi-wna",
    "exit permit|rekomendasi visa": "https://kemlu.go.id/etc/exit-permit-dan-rekomendasi-visa",
    "exit permit|visa recommendation": "https://kemlu.go.id/etc/exit-permit-dan-rekomendasi-visa",
    "csca|country signing certificate authority": "https://kemlu.go.id/layanan/layanan-konsuler-fasilitas-diplomatik-dan-pelindungan-wni/country-signing-certificate-authority-csca",
    "fasilitas kendaraan": "https://kemlu.go.id/etc/fasilitas-kendaraan",
    "vehicle facilities": "https://kemlu.go.id/etc/fasilitas-kendaraan",
    "pendaftaran, kunjungan regional dan fasilitas akreditasi": "https://kemlu.go.id/etc/pendaftaran-kunjungan-regional-dan-fasilitas-akreditasi",
    "registration, regional visits and facility accreditation": "https://kemlu.go.id/etc/pendaftaran-kunjungan-regional-dan-fasilitas-akreditasi",
    "perizinan bangunan": "https://kemlu.go.id/etc/perizinan-bangunan",
    "building permit": "https://kemlu.go.id/etc/perizinan-bangunan",
    "senjata api dan radio": "https://kemlu.go.id/etc/senjata-api-dan-frekuensi-radio",
    "firearms and radio frequencies": "https://kemlu.go.id/etc/senjata-api-dan-frekuensi-radio",
    "fasilitasi importasi dan eksportasi barang bagi kantor pna dan oi di indonesia": "https://kemlu.go.id/etc/pelayanan-fasilitasi-importasi-dan-eksportasi-barang-bagi-kantor-pna-dan-oi-di-indonesia",
    "import and export facilitation for pna and io offices in indonesia": "https://kemlu.go.id/etc/pelayanan-fasilitasi-importasi-dan-eksportasi-barang-bagi-kantor-pna-dan-oi-di-indonesia",
    "rekomendasi pas bandara tahunan": "https://kemlu.go.id/etc/pelayanan-rekomendasi-pas-bandara-tahunan",
    "annual airport pass recommendation": "https://kemlu.go.id/etc/pelayanan-rekomendasi-pas-bandara-tahunan",
    "penerbitan id card": "https://kemlu.go.id/etc/pelayanan-penerbitan-id-card",
    "id card issuance": "https://kemlu.go.id/etc/pelayanan-penerbitan-id-card",
    "perpajakan": "https://kemlu.go.id/etc/perpajakan",
    "taxation": "https://kemlu.go.id/etc/perpajakan",
}

LLM_API_URL = "https://openrouter.ai/api/v1/chat/completions"
app.config['LLM_API_KEY'] = os.environ.get("LLM_API_KEY")
app.config['LLM_MODEL'] = os.environ.get("LLM_MODEL", "deepseek/deepseek-chat")
app.config['LLM_TIMEOUT'] = int(os.environ.get("LLM_TIMEOUT", 30))

conversation_histories = {}
session_contexts = {}
session_triggered_keywords = {}

# --- HELPER FUNCTIONS ---

def build_link_map():
    """
    Inisialisasi LINK_MAP dari MASTER_LINK_MAP dan melengkapinya dengan data dari keywords.
    """
    global LINK_MAP
    LINK_MAP = MASTER_LINK_MAP.copy()
    
    href_pattern = re.compile(r'href=[\'"](.*?)[\'"]')
    all_keywords = KEYWORDS_ID + KEYWORDS_EN
    for item in all_keywords:
        context_key = item.get("context")
        answer = item.get("answer", "")
        if not context_key or not isinstance(answer, str):
            continue
        if context_key.lower() not in LINK_MAP:
            found_links = href_pattern.findall(answer)
            if found_links:
                LINK_MAP[context_key.lower()] = found_links[0]
    
    logging.info(f"Link map built successfully. Total links: {len(LINK_MAP)}")
    logging.debug(f"LINK_MAP content: {LINK_MAP}")

def replace_link_placeholders(text: str) -> str:
    """
    Mengganti placeholder [LINK:context] dengan tag HTML <a> menggunakan LINK_MAP.
    """
    if not isinstance(text, str): return text

    def replacer(match):
        context_key = match.group(1).strip().lower()
        url = LINK_MAP.get(context_key)
        
        if url:
            link_text = match.group(1).strip().title()
            return f'<a href="{url}" target="_blank">{link_text}</a>'
        else:
            logging.warning(f"No link found in LINK_MAP for placeholder key: '{context_key}'")
            return match.group(1).strip()

    placeholder_pattern = re.compile(r'\[LINK:(.*?)\]', re.IGNORECASE)
    return placeholder_pattern.sub(replacer, text)

def log_activity(session_id, user_input, bot_response, response_type, lang):
    """Mencatat aktivitas interaksi ke Firestore."""
    if not db: return
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
    """Mengonversi Markdown sederhana (bold) ke HTML."""
    if not isinstance(text, str): return text
    text = re.sub(r'\*\*(.*?)\*\*', r'<strong>\1</strong>', text)
    return text

def get_accurate_maps_url(address: str) -> str:
    """Membuat URL pencarian Google Maps."""
    base_url = "https://www.google.com/maps/search/?api=1&query="
    encoded_address = quote_plus(address)
    return base_url + encoded_address

def format_perwakilan_list_items(info: dict, lang: str) -> str:
    """Memformat detail kantor perwakilan menjadi item list HTML (<li>)."""
    maps_link = get_accurate_maps_url(info.get('address', ''))
    
    labels = {
        "id": {"address": "Alamat", "map_text": "Lihat di Peta", "accreditation": "Wilayah Akreditasi", "phone": "Telepon", "fax": "Fax", "email": "Email", "website": "Situs Web"},
        "en": {"address": "Address", "map_text": "View on Map", "accreditation": "Accreditation Area", "phone": "Phone", "fax": "Fax", "email": "Email", "website": "Website"}
    }
    l = labels.get(lang, labels['id'])
    
    items = []
    if info.get("address"):
        items.append(f"<li><b>{l['address']}:</b> {info['address']} <a href='{maps_link}' target='_blank'>({l['map_text']})</a></li>")
    if info.get("wilayah_akreditasi"):
        items.append(f"<li><b>{l['accreditation']}:</b> {info['wilayah_akreditasi']}</li>")
    if info.get("telepon"):
        items.append(f"<li><b>{l['phone']}:</b> {info['telepon']}</li>")
    if info.get("fax"):
        items.append(f"<li><b>{l['fax']}:</b> {info['fax']}</li>")
    if info.get("email"):
        items.append(f"<li><b>{l['email']}:</b> {info['email']}</li>")
    if info.get("link"):
        items.append(f"<li><b>{l['website']}:</b> <a href='{info['link']}' target='_blank'>{info['link']}</a></li>")
        
    return "".join(items)

def get_llm_response(messages: list, lang: str = "id", context: str = "") -> tuple[str | None, list]:
    """Mendapatkan respons dari LLM API."""
    api_key = app.config.get('LLM_API_KEY')
    if not api_key:
        logging.error("LLM_API_KEY is not set. Skipping LLM call.")
        return None, []

    system_content = (f"{LLM_SYSTEM_PROMPTS.get(lang, LLM_SYSTEM_PROMPTS['id'])}\n\n{context}\n\n{LLM_FOLLOW_UP_INSTRUCTIONS.get(lang, LLM_FOLLOW_UP_INSTRUCTIONS['id'])}")
    system_prompt = [{"role": "system", "content": system_content}]
    headers = {"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"}
    payload = {"model": app.config.get('LLM_MODEL'), "messages": system_prompt + messages, "max_tokens": 1536, "temperature": 0.2}

    max_retries, base_delay = 3, 1
    for attempt in range(max_retries):
        try:
            response = requests.post(LLM_API_URL, json=payload, headers=headers, timeout=app.config.get('LLM_TIMEOUT'))
            if response.status_code == 429:
                delay = base_delay * (2 ** attempt)
                logging.warning(f"Rate limit exceeded. Retrying in {delay}s...")
                time.sleep(delay)
                continue
            response.raise_for_status()
            data = response.json()
            full_content = data.get("choices", [{}])[0].get("message", {}).get("content", "").strip()
            logging.info(f"Raw full content from LLM: {full_content}")
            if RESPONSE_SEPARATOR in full_content:
                main_answer, follow_up_raw = full_content.split(RESPONSE_SEPARATOR, 1)
                follow_ups = [q.strip() for q in follow_up_raw.split('|') if q.strip().endswith('?')]
                return main_answer.strip(), follow_ups[:3]
            return full_content, []
        except requests.exceptions.RequestException as e:
            logging.error(f"LLM API call failed on attempt {attempt + 1}: {e}")
            if hasattr(e, 'response') and e.response:
                logging.error(f"LLM API Response: {e.response.status_code} - {e.response.text}")
            if attempt < max_retries - 1:
                time.sleep(base_delay * (2 ** attempt))
            else:
                return None, []
    return None, []

def get_static_fallback(user_input_lower: str, lang: str) -> tuple[str, str] | None:
    """Memberikan respons statis jika LLM gagal."""
    fallbacks = STATIC_FALLBACKS.get(lang, {})
    for pattern, answer in fallbacks.items():
        if re.search(pattern, user_input_lower):
            logging.warning(f"LLM failed, providing static fallback for pattern: {pattern}")
            return answer, "static_fallback"
    return None, None

def add_contextual_hyperlinks(reply_text: str, session_id: str, lang: str) -> str:
    """
    Menambahkan hyperlink "baca selengkapnya" sebagai footer di akhir respons.
    """
    triggered_contexts = session_triggered_keywords.get(session_id, set())
    if not triggered_contexts:
        return reply_text       

    links_to_add = []
    
    for context in triggered_contexts:
        context_key = context.lower()
        url = LINK_MAP.get(context_key)
        
        if url:
            labels = {
                "id": {"intro": "Untuk informasi lebih lanjut, silakan kunjungi"},
                "en": {"intro": "For more information, please visit"}
            }
            l = labels.get(lang, labels['id'])
            
            link_html = (
                f'<p>{l["intro"]} <a href="{url}" target="_blank">{context.title()}</a>.</p>'
            )
            links_to_add.append(link_html)

    if links_to_add:
        footer_html = "<hr>" + "".join(links_to_add)
        return reply_text + footer_html
        
    return reply_text

def retrieve_relevant_info(query: str, threshold=0.3) -> dict | None:
    """
    Mencari informasi paling relevan dari knowledge base menggunakan TF-IDF.
    Ini adalah langkah 'Retrieve' dalam RAG.
    Mengembalikan seluruh item kamus yang cocok.
    """
    try:
        query_vector = vectorizer.transform([query])
        cosine_similarities = cosine_similarity(query_vector, tfidf_matrix).flatten()
        most_similar_doc_index = cosine_similarities.argmax()
        highest_score = cosine_similarities[most_similar_doc_index]

        logging.info(f"RAG retrieval score for '{query}': {highest_score:.2f} (Threshold: {threshold})")

        if highest_score > threshold:
            retrieved_item = knowledge_base[most_similar_doc_index]
            logging.info(f"RAG context retrieved for pattern: '{retrieved_item['pattern']}'")
            return retrieved_item
            
    except Exception as e:
        logging.error(f"Error during RAG retrieval: {e}")

    return None

# --- CORE MESSAGE PROCESSING LOGIC ---

def handle_address_request(user_input_lower: str, lang: str) -> tuple[str, list, str, str] | None:
    """Menangani permintaan alamat perwakilan dengan detail lengkap."""
    address_match = re.search(ADDRESS_KEYWORDS_PATTERN, user_input_lower, re.IGNORECASE)
    if not address_match:
        return None
        
    location_name = address_match.groups()[-1].strip()
    info, score = find_location_info(location_name)
    
    if info and score > 80:
        list_items = format_perwakilan_list_items(info, lang)
        title = f"Informasi untuk {info['name']}" if lang == 'id' else f"Information for {info['name']}"
        follow_ups = ["Apa saja jam layanan konsuler?", "Apakah saya perlu membuat janji temu?"] if lang == "id" else ["What are the consular service hours?", "Do I need an appointment?"]
        return f"<strong>{title}</strong><ul>{list_items}</ul>", follow_ups, "address_request", info['name']
    return None

def handle_lost_document(user_input_lower: str, lang: str) -> tuple[str, list, str, str] | None:
    """Menangani permintaan tentang dokumen hilang dengan info kontak detail."""
    if not re.search(LOST_DOCUMENT_PATTERN, user_input_lower):
        return None
    
    location_name = ""
    location_match = re.search(r"(di|in)\s+([\w\s]+)", user_input_lower)
    if location_match:
        location_name = location_match.group(2).strip()

    info, score = (find_location_info(location_name) if location_name else (None, 0))

    if info and score > 80:
        list_items = format_perwakilan_list_items(info, lang)
        if lang == "en":
            title, intro = f"Guidance for Lost Document in {info['name']}", f"<p>You should immediately contact <b>{info['name']}</b> for assistance. Below are their contact details:</p>"
            follow_ups = ["What are the requirements for an Emergency Travel Document?", "How much does it cost?", "What are the opening hours?"]
        else:
            title, intro = f"Panduan Kehilangan Dokumen di {info['name']}", f"<p>Anda harus segera menghubungi <b>{info['name']}</b> untuk bantuan. Berikut detail kontak mereka:</p>"
            follow_ups = ["Apa saja syarat mengurus SPLP?", "Berapa biayanya?", "Apa saja jam bukanya?"]
        return f"<strong>{title}</strong>{intro}<ul>{list_items}</ul>", follow_ups, "lost_document", info['name']

    default_reply_text = ("Saya memahami Anda kehilangan dokumen. Mohon informasikan di kota dan negara mana Anda berada agar saya dapat membantu lebih lanjut.", ["Saya kehilangan paspor di Berlin", "Dokumen saya hilang di Singapura"]) if lang == "id" else ("I understand you've lost a document. To help, please tell me which city and country you are in.", ["I lost my passport in Berlin", "My document is missing in Singapore"])
    return default_reply_text[0], default_reply_text[1], "lost_document_generic", "dokumen hilang"

def process_user_message(user_input: str, lang: str, session_id: str) -> tuple[str | None, list, str, str | None]:
    """Memproses pesan pengguna dan menentukan respons yang sesuai."""
    user_input_lower = user_input.lower()
    
    if re.search(GREETING_PATTERN, user_input_lower):
        return GREETINGS.get(lang), GENERIC_FOLLOW_UPS.get(lang, []), "greeting", None

    response = handle_address_request(user_input_lower, lang)
    if response:
        return response[0], response[1], response[2], response[3]

    response = handle_lost_document(user_input_lower, lang)
    if response:
        return response[0], response[1], response[2], response[3]

    keywords_list = sorted(KEYWORDS_ID if lang == "id" else KEYWORDS_EN, key=lambda x: x['priority'], reverse=True)
    for item in keywords_list:
        if re.search(item['pattern'], user_input_lower):
            if item.get("context"):
                session_triggered_keywords.setdefault(session_id, set()).add(item['context'])
            return item["answer"], item["follow_up"], "keyword_match", item.get("context")
            
    return None, [], "llm_fallback", None

# --- FLASK ROUTES (API ENDPOINTS) ---
@app.route("/")
def index():
    """Merender halaman utama chatbot."""
    return render_template("index.html")

@app.route("/ask", methods=["POST"])
def ask():
    """Endpoint utama untuk menerima dan merespons pesan chatbot."""
    data = request.get_json()
    if not data: return jsonify({"error": "Invalid JSON"}), 400
    
    user_input_original = data.get("message", "").strip()
    lang = data.get("language", "id")
    session_id = data.get("session_id")
    if not session_id: return jsonify({"reply": "Error: session_id is missing.", "follow_up": []}), 400
    
    session_triggered_keywords.pop(session_id, None)
    
    contexts = session_contexts.get(session_id, [])
    last_context = contexts[-1] if contexts else None
    history = conversation_histories.setdefault(session_id, [])
    
    reply_text, follow_up_questions, response_type, context_from_processor = None, [], 'llm', None
    user_input_for_llm = user_input_original

    is_new_topic = re.search(GREETING_PATTERN, user_input_original.lower()) or \
                   re.search(ADDRESS_KEYWORDS_PATTERN, user_input_original.lower()) or \
                   re.search(LOST_DOCUMENT_PATTERN, user_input_original.lower())

    if last_context and not is_new_topic:
        logging.info(f"Prioritizing as a contextual follow-up for '{last_context}'.")
        session_triggered_keywords.setdefault(session_id, set()).add(last_context)
        user_input_for_llm = f"Terkait {last_context}, {user_input_original}" if lang == "id" else f"Regarding {last_context}, {user_input_original}"
        response_type = 'llm_follow_up'
    else:
        if is_new_topic and last_context:
            logging.info(f"Context breaker detected. Clearing old context for session {session_id}.")
            session_contexts[session_id] = []
        logging.info("Processing as a new query.")
        reply_text, follow_up_questions, response_type, context_from_processor = process_user_message(user_input_original, lang, session_id)

    if context_from_processor:
        current_contexts = session_contexts.setdefault(session_id, [])
        if not current_contexts or current_contexts[-1] != context_from_processor:
             current_contexts.append(context_from_processor)
        session_contexts[session_id] = current_contexts[-3:]
        logging.info(f"Context updated for session {session_id}: {session_contexts[session_id]}")

    if not reply_text:
        retrieved_item = retrieve_relevant_info(user_input_original)
        response_type = "llm_rag_fallback"

        if retrieved_item:
            retrieved_answer = retrieved_item['answer']
            retrieved_context_key = retrieved_item.get('context')

            if retrieved_context_key:
                session_triggered_keywords.setdefault(session_id, set()).add(retrieved_context_key)
                logging.info(f"RAG flow triggered context: '{retrieved_context_key}'")

            rag_prompt_message = (
                f"Anda adalah asisten AI yang membantu. Jawab pertanyaan pengguna HANYA berdasarkan "
                f"informasi dalam 'Konteks' yang diberikan. Jangan gunakan pengetahuan lain. "
                f"Jika jawaban tidak ada di dalam konteks, katakan Anda tidak tahu.\n\n"
                f"--- Konteks ---\n{retrieved_answer}\n\n"
                f"--- Pertanyaan Pengguna ---\n{user_input_original}"
            )
            llm_answer, llm_follow_ups = get_llm_response(
                [{"role": "user", "content": rag_prompt_message}], lang
            )
        else:
            logging.info("RAG retrieval failed, using generic LLM fallback.")
            response_type = "llm_generic_fallback"
            
            cache_key = f"{lang}:{user_input_for_llm.lower()}"
            if cache_key in llm_cache and (datetime.now() - llm_cache[cache_key][1]).total_seconds() < CACHE_TTL_SECONDS:
                logging.info(f"Serving generic response from cache for key: {cache_key}")
                llm_answer, llm_follow_ups = llm_cache[cache_key][0]
                llm_cache.move_to_end(cache_key)
            else:
                logging.info(f"Cache miss for generic query. Calling LLM API for: '{user_input_for_llm}'")
                llm_context_prompt = f"Current conversation context is about: {session_contexts.get(session_id, [])[-1]}." if session_contexts.get(session_id) else ""
                llm_answer, llm_follow_ups = get_llm_response(history + [{"role": "user", "content": user_input_for_llm}], lang, context=llm_context_prompt)
                if llm_answer:
                    llm_cache[cache_key] = ((llm_answer, llm_follow_ups), datetime.now())
                    if len(llm_cache) > MAX_CACHE_SIZE: llm_cache.popitem(last=False)

        if llm_answer:
            processed_text = replace_link_placeholders(llm_answer)
            reply_text = convert_markdown_to_html(processed_text)
            follow_up_questions = llm_follow_ups
        else:
            logging.error("LLM call failed after retries. Using static fallback.")
            reply_text, response_type_fallback = get_static_fallback(user_input_original.lower(), lang)
            if not reply_text:
                reply_text = GENERIC_FALLBACK.get(lang)
                response_type = "generic_fallback_final"
            else:
                response_type = response_type_fallback
            follow_up_questions = GENERIC_FOLLOW_UPS.get(lang, [])

    if reply_text:
        reply_text = add_contextual_hyperlinks(reply_text, session_id, lang)

    history.extend([{"role": "user", "content": user_input_original}, {"role": "assistant", "content": reply_text}])
    conversation_histories[session_id] = history[-MAX_CONVERSATION_HISTORY:]
    
    log_activity(session_id, user_input_original, reply_text, response_type, lang)
    
    return jsonify({"reply": reply_text, "follow_up": follow_up_questions})

@app.route('/report', methods=['POST'])
def report():
    """Menerima laporan/feedback dari pengguna."""
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
    """Menerima rating dari pengguna."""
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
    build_link_map()
    app.run(host='0.0.0.0', port=5000, debug=False)