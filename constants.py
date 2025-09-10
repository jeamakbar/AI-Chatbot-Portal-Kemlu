# --- APPLICATION CONSTANTS ---
LLM_API_URL = "https://openrouter.ai/api/v1/chat/completions"
RESPONSE_SEPARATOR = "###"
MAX_CONVERSATION_HISTORY = 10

# --- REGEX PATTERNS ---
ADDRESS_KEYWORDS_PATTERN = r"(alamat|lokasi|di mana|address|location|where is|dimana).*(kbri|konsulat|kedutaan|perwakilan|kdei|embassy|consulate|representation)[\w\s]*((di|di negara|untuk)\s*)?([\w\s\.]+)$"
GREETING_PATTERN = r"^\s*(hi|hello|halo|selamat\s(pagi|siang|sore|malam))\s*$"
LOST_DOCUMENT_PATTERN = r"kehilangan|hilang|lost|missing"


# --- CENTRALIZED MESSAGES ---
GREETINGS = {
    "id": "Halo! Ada yang bisa saya bantu?",
    "en": "Hello! How can I help you?"
}

GENERIC_FOLLOW_UPS = {
    "id": ["Saya mau tanya tentang paspor", "Di mana alamat KBRI di Tokyo?", "Bagaimana cara lapor diri?"],
    "en": ["I want to ask about passports", "Where is the embassy in Tokyo?", "How do I register my stay abroad?"]
}

# --- TIERED FALLBACK MESSAGES ---
STATIC_FALLBACKS = {
    "id": {
        r"paspor|visa|legalisasi|konsuler": (
            "<strong>Layanan Konsuler</strong><br>"
            "Maaf, sistem AI sedang mengalami kendala untuk menjawab detail pertanyaan Anda. "
            "Untuk informasi paling akurat mengenai layanan konsuler (paspor, visa, legalisasi), silakan kunjungi langsung "
            '<a href="https://kemlu.go.id/layanan/layanan-konsuler-fasilitas-diplomatik-dan-pelindungan-wni/kekonsuleran" target="_blank">halaman Layanan Konsuler di situs resmi Kemlu</a>.'
        ),
        r"alamat|lokasi|kbri|kjri|kedutaan|konsulat": (
            "<strong>Informasi Perwakilan RI</strong><br>"
            "Maaf, sistem AI sedang mengalami kendala untuk mencari alamat spesifik saat ini. "
            "Anda dapat menemukan daftar lengkap alamat seluruh Perwakilan RI (KBRI, KJRI, PTRI) di "
            '<a href="https://kemlu.go.id/perwakilan" target="_blank">halaman Perwakilan di situs resmi Kemlu</a>.'
        ),
        r"bantuan|pelindungan|darurat|lapor diri": (
            "<strong>Pelindungan WNI</strong><br>"
            "Maaf, sistem AI sedang mengalami kendala. Untuk urusan darurat, pelindungan, atau lapor diri, "
            "silakan akses <a href='https://peduliwni.kemlu.go.id' target='_blank'>portal Peduli WNI</a> atau hubungi langsung Perwakilan RI terdekat."
        )
    },
    "en": {
        r"passport|visa|legalization|consular": (
            "<strong>Consular Services</strong><br>"
            "Sorry, the AI system is currently unable to answer your specific question. "
            "For the most accurate information regarding consular services (passports, visas, legalization), please visit the "
            '<a href="https://kemlu.go.id/layanan/layanan-konsuler-fasilitas-diplomatik-dan-pelindungan-wni/kekonsuleran" target="_blank">Consular Services page on the official Kemlu website</a>.'
        ),
        r"address|location|embassy|consulate": (
            "<strong>Indonesian Mission Information</strong><br>"
            "Sorry, the AI system is currently unable to find a specific address. "
            "You can find a complete list of all Indonesian Missions (Embassies and Consulates) on the "
            '<a href="https://kemlu.go.id/perwakilan" target="_blank">Missions page on the official Kemlu website</a>.'
        ),
        r"help|protection|emergency|report": (
            "<strong>Citizen Protection</strong><br>"
            "Sorry, the AI system is currently unavailable. For emergencies, protection, or self-registration, "
            "please access the <a href='https://peduliwni.kemlu.go.id' target='_blank'>Peduli WNI portal</a> or contact the nearest Indonesian Mission directly."
        )
    }
}

GENERIC_FALLBACK = {
    "id": (
        "Maaf, saya sedang mengalami kendala teknis saat ini. Mohon coba sampaikan pertanyaan Anda dengan kalimat yang berbeda. "
        'Jika masalah berlanjut, Anda dapat mencari informasi langsung di <a href="https://kemlu.go.id" target="_blank">situs resmi Kemlu</a>.'
    ),
    "en": (
        "I am currently experiencing technical difficulties. Please try rephrasing your question. "
        'If the problem persists, you can find information directly on the <a href="https://kemlu.go.id" target="_blank">official Kemlu website</a>.'
    )
}


# --- LLM PROMPTS ---
LLM_SYSTEM_PROMPTS = {
    "en": (
        "## Persona\n"
        "You are 'Sahabat Kemlu', the highly professional, empathetic, and accurate AI Virtual Assistant for the Ministry of Foreign Affairs of the Republic of Indonesia. Your primary role is to provide clear, reliable, and concise information regarding all services offered by the Ministry and its representative offices (Embassies/KBRI and Consulate Generals/KJRI) worldwide. Your communication style is formal yet friendly.\n\n"
        "## Core Directives\n"
        "1.  **Absolute Source of Truth:** All your answers **must** be derived **exclusively** from the content available on `kemlu.go.id` and the internal data provided in the local context. Do not invent information or use external knowledge.\n"
        "2.  **Prioritize Internal Data:** You have access to a local data context with specific keywords and structured information. If a user's query matches a keyword (e.g., passport renewal, address of an embassy), you **must** use the provided internal data for the answer. When you use this data, start your response with a clear statement, such as: `Based on our available data, here is the information for...`\n"
        "3.  **Strict Scope of Service:** Your function is strictly limited to the services of the Ministry of Foreign Affairs of Indonesia. If a query is outside this scope (e.g., domestic policies, other ministries, personal opinions), you **must** reply with the exact disclaimer: \"I can only provide information regarding the services of the Ministry of Foreign Affairs of the Republic of Indonesia and its representatives abroad. For other matters, please consult the relevant authorities.\"\n"
        "4.  **Handling Missing Information:** If a query is within scope but the information is not on `kemlu.go.id` or in the internal data, you **must** reply with: \"Information regarding your query is not available on the kemlu.go.id website. For the most accurate details, please visit the official website directly or contact the nearest Indonesian Representative Office.\"\n"
        "5.  **Global & Specific Queries:** Provide general information applicable to all locations unless a specific city or country is mentioned. If a query is ambiguous (e.g., 'visa requirements'), provide general information first and then suggest follow-up questions to narrow it down.\n\n"
        "## Absolute Response Structure (Strict HTML Enforcement)\n"
        "Your response must be clean, structured, and easy to read. Adhere to these HTML rules without exception:\n"
        "1.  **Main Title (Mandatory):** Every response **must** start with a relevant, bolded title. **Format:** `<strong>Service Title</strong>`.\n"
        "2.  **Introduction:** Provide a brief one-sentence introduction after the title.\n"
        "3.  **Structured Lists:** All details (requirements, steps, documents) **must** be presented in an unordered list (`<ul>`). **Format:** `<ul><li>Detail 1</li><li>Detail 2</li></ul>`.\n"
        "4.  **Clear Labels:** Within each list item, the information category **must** be bolded. **Format:** `<li><strong>Address:</strong> Lehrter Str. 16-17, 10557 Berlin, Germany</li>`.\n"
        "5.  **Mandatory Map Link:** Any physical address **must** be immediately followed by a direct Google Maps link. **Format:** `<a href=\"https://www.google.com/maps/search/?api=1&query=Lehrter+Str.+16-17%2C+10557+Berlin%2C+Germany\" target=\"_blank\">View on Google Maps</a>`.\n"
        "6.  **Important Notes:** Use `<em>` tags for important notes or disclaimers at the end of the list.\n\n"
    ),
    "id": (
        "## Persona\n"
        "Anda adalah 'Sahabat Kemlu', Asisten Virtual AI dari Kementerian Luar Negeri RI yang sangat profesional, empatik, dan akurat. Peran utama Anda adalah memberikan informasi yang jelas, terpercaya, dan ringkas mengenai keseluruhan layanan Kementerian Luar Negeri dan semua perwakilannya (KBRI dan KJRI) di seluruh dunia. Gaya komunikasi Anda formal namun tetap ramah.\n\n"
        "## Arahan Utama\n"
        "1.  **Sumber Tunggal Absolut:** Semua jawaban Anda **wajib** bersumber **eksklusif** dari konten yang tersedia di `kemlu.go.id` dan data internal yang diberikan dalam konteks lokal. Jangan mengarang informasi atau menggunakan pengetahuan eksternal.\n"
        "2.  **Prioritaskan Data Internal:** Anda memiliki akses ke data lokal berisi kata kunci spesifik dan informasi terstruktur. Jika pertanyaan pengguna cocok dengan kata kunci (misal: perpanjang paspor, alamat kedutaan), Anda **wajib** menggunakan data internal tersebut. Saat menggunakan data ini, awali jawaban Anda dengan kalimat yang jelas, seperti: `Berdasarkan data yang kami miliki, berikut adalah informasinya...`\n"
        "3.  **Lingkup Layanan yang Ketat:** Fungsi Anda terbatas secara ketat pada layanan Kementerian Luar Negeri RI. Jika pertanyaan di luar lingkup ini (misal: kebijakan dalam negeri, kementerian lain, opini pribadi), Anda **wajib** membalas dengan disclaimer resmi berikut: \"Saya hanya dapat memberikan informasi seputar layanan Kementerian Luar Negeri RI dan perwakilannya di luar negeri. Untuk urusan lain, silakan hubungi pihak yang berwenang.\"\n"
        "4.  **Penanganan Informasi Nihil:** Jika informasi yang dicari masih dalam lingkup Kemlu namun tidak ada di `kemlu.go.id` atau data internal, Anda **wajib** membalas dengan kalimat: \"Informasi mengenai permintaan Anda tidak tersedia di situs kemlu.go.id. Untuk detail yang paling akurat, silakan kunjungi situs web resmi secara langsung atau hubungi Perwakilan RI terdekat.\"\n"
        "5.  **Pertanyaan Global & Spesifik:** Berikan informasi umum yang berlaku di semua lokasi, kecuali jika pengguna menyebutkan kota atau negara tertentu. Jika pertanyaan ambigu (misal: 'syarat visa'), berikan informasi umum terlebih dahulu, lalu sarankan pertanyaan lanjutan untuk mengerucutkannya.\n\n"
        "## Struktur Jawaban Absolut (Wajib Menggunakan HTML)\n"
        "Struktur jawaban harus rapi dan mudah dibaca. Patuhi aturan HTML berikut tanpa kecuali:\n"
        "1.  **Judul Utama (Wajib):** Setiap jawaban **wajib** diawali dengan judul yang relevan dan ditebalkan. **Format:** `<strong>Judul Layanan</strong>`.\n"
        "2.  **Pengantar:** Berikan satu kalimat pengantar singkat setelah judul.\n"
        "3.  **Daftar Terstruktur:** Semua detail (persyaratan, alamat, langkah) **wajib** disajikan dalam bentuk daftar tidak berurutan (`<ul>`). **Format:** `<ul><li>Detail 1</li><li>Detail 2</li></ul>`.\n"
        "4.  **Label yang Jelas:** Di dalam setiap item daftar, kategori informasi **wajib** ditebalkan. **Format:** `<li><strong>Alamat:</strong> Lehrter Str. 16-17, 10557 Berlin, Germany</li>`.\n"
        "5.  **Tautan Peta (Wajib):** Setiap alamat fisik **wajib** diikuti dengan tautan pencarian Google Maps. **Format:** `<a href=\"https://www.google.com/maps/search/?api=1&query=Lehrter+Str.+16-17%2C+10557+Berlin%2C+Germany\" target=\"_blank\">Lihat di Google Maps</a>`.\n"
        "6.  **Catatan Penting:** Gunakan tag `<em>` untuk catatan penting atau disclaimer di akhir daftar.\n\n"
    )
}

LLM_FOLLOW_UP_INSTRUCTIONS = {
    "en": (
        f"After your main answer, add a separator '{RESPONSE_SEPARATOR}' and then suggest up to 3 relevant, concise, and helpful follow-up questions the user might have. "
        "Each question must end with a question mark. Example: ### What are the opening hours?|Do I need an appointment?|How much does it cost?"
    ),
    "id": (
        f"Setelah jawaban utama Anda, tambahkan pemisah '{RESPONSE_SEPARATOR}' lalu sarankan hingga 3 pertanyaan lanjutan yang relevan, ringkas, dan membantu. "
        "Setiap pertanyaan harus diakhiri dengan tanda tanya. Contoh: ### Apa saja jam bukanya?|Apakah saya perlu membuat janji temu?|Berapa biayanya?"
    )
}

# --- STRUCTURED KEYWORD DATA ---

KEYWORDS_ID = [
    # ... (keyword lapor diri dan paspor tetap sama) ...
    {
        "pattern": r"lapor diri",
        "priority": 10,
        "context": "lapor diri",
        "answer": (
            "<strong>Prosedur Lapor Diri Online untuk WNI di Luar Negeri</strong><br><br>"
            "Warga Negara Indonesia (WNI) yang berada di luar negeri dapat melakukan Lapor Diri secara daring melalui portal resmi Kementerian Luar Negeri. Berikut langkah-langkahnya:<br><br>"
            "📝 <strong>Langkah-langkah Lapor Diri Online:</strong>"
            "<ul>"
            "<li>Kunjungi situs resmi Peduli WNI di: <a href='https://peduliwni.kemlu.go.id' target='_blank'>https://peduliwni.kemlu.go.id</a></li>"
            "<li><strong>Buat Akun atau Masuk:</strong> Jika belum memiliki akun, silakan mendaftar terlebih dahulu.</li>"
            "<li><strong>Isi Formulir:</strong> Isi formulir Lapor Diri secara lengkap dengan data pribadi, informasi paspor, alamat tinggal di luar negeri, dan kontak darurat.</li>"
            "<li><strong>Unggah Dokumen:</strong> Siapkan dan unggah dokumen pendukung seperti salinan paspor dan bukti izin tinggal (contoh: visa atau green card).</li>"
            "<li><strong>Simpan Bukti:</strong> Setelah selesai, pastikan Anda menyimpan bukti registrasi Lapor Diri Anda.</li>"
            "</ul>"
            "💡 <strong>Manfaat Lapor Diri:</strong>"
            "<ul>"
            "<li>Memudahkan Perwakilan RI (KBRI/KJRI) dalam memberikan layanan dan perlindungan.</li>"
            "<li>Menjadi salah satu persyaratan untuk pengajuan layanan kekonsuleran seperti perpanjangan paspor, surat keterangan, dan legalisasi dokumen.</li>"
            "</ul>"
        ),
        "follow_up": ["Dokumen apa saja yang perlu diunggah?", "Apakah lapor diri itu wajib?", "Berapa lama proses verifikasi lapor diri?"]
    },
    {
        "pattern": r"(prosedur|syarat|cara|membuat|perpanjang|biometrik|dokumen).*(paspor)",
        "priority": 10,
        "context": "paspor",
        "answer": (
            "<strong>Berikut adalah langkah-langkah dan persyaratan umum untuk mengajukan atau memperpanjang paspor Indonesia:</strong><br><br>"
            "📝 <strong>Langkah-langkah Pengajuan/Perpanjangan Paspor:</strong>"
            "<ul>"
            "<li><strong>Buat Janji Temu Online:</strong> Buat janji temu (antrean) melalui situs web atau aplikasi resmi Kantor Imigrasi (untuk di dalam negeri) atau Perwakilan RI/KBRI/KJRI (untuk di luar negeri).</li>"
            "<li><strong>Datang ke Lokasi:</strong> Hadir di kantor imigrasi atau Perwakilan RI yang dipilih sesuai jadwal untuk proses verifikasi data, pengambilan foto, dan sidik jari (biometrik).</li>"
            "<li><strong>Wawancara Singkat:</strong> Petugas akan melakukan wawancara singkat untuk verifikasi.</li>"
            "<li><strong>Lakukan Pembayaran:</strong> Setelah semua proses selesai, Anda akan diminta untuk membayar biaya paspor sesuai ketentuan yang berlaku.</li>"
            "</ul>"
            "📄 <strong>Dokumen yang Harus Dibawa (Asli dan Fotokopi):</strong>"
            "<ul>"
            "<li><strong>KTP Elektronik</strong> yang masih berlaku.</li>"
            "<li><strong>Kartu Keluarga (KK)</strong>.</li>"
            "<li><strong>Salah satu dari dokumen berikut:</strong> Akta Kelahiran, Ijazah (SD/SMP/SMA), atau Buku Nikah. Pastikan nama, tempat/tanggal lahir, dan nama orang tua tercantum dengan jelas.</li>"
            "<li><strong>Paspor Lama:</strong> Wajib dibawa jika Anda ingin memperpanjang paspor.</li>"
            "</ul>"
            "⚠️ <strong>Catatan Penting:</strong>"
            "<ul>"
            "<li>Pastikan semua data pada dokumen (KTP, KK, Akta/Ijazah) konsisten.</li>"
            "<li>Untuk pengajuan di luar negeri, prosedur dan persyaratan mungkin sedikit berbeda. Silakan hubungi Perwakilan RI terdekat untuk informasi lebih lanjut.</li>"
            '<li>Informasi lebih detail mengenai layanan kekonsuleran dapat ditemukan di <a href="https://kemlu.go.id/layanan/layanan-konsuler-fasilitas-diplomatik-dan-pelindungan-wni/kekonsuleran" target="_blank">halaman Kekonsuleran Kemlu</a>.</li>'
            "</ul>"
        ),
        "follow_up": ["Berapa biaya pembuatan paspor?", "Berapa lama prosesnya sampai paspor jadi?", "Apa bedanya paspor biasa dan e-paspor?"]
    },
     {
        "pattern": r"(syarat|prosedur|cara|biaya).*(legalisasi|legalisir).*(dokumen)",
        "priority": 9,
        "context": "legalisasi dokumen",
        "answer": (
            "<strong>Layanan Legalisasi Dokumen</strong><br>"
            "Tentu. Legalisasi adalah proses pengesahan tanda tangan pejabat dan/atau segel resmi pada dokumen. Perlu diingat, proses ini tidak mengesahkan kebenaran isi dokumen.<br><br>"
            "<strong>Alur Umum Legalisasi Dokumen Indonesia untuk Penggunaan di Luar Negeri:</strong>"
            "<ul>"
            "<li><strong>Tahap 1: Kementerian Hukum dan HAM (Kemenkumham)</strong><br>Dokumen asli harus terlebih dahulu dilegalisasi oleh Direktorat Perdata di Kemenkumham RI. Permohonan umumnya dilakukan secara online melalui situs AHU Online.</li>"
            "<li><strong>Tahap 2: Kementerian Luar Negeri (Kemenlu)</strong><br>Setelah disahkan Kemenkumham, dokumen dibawa ke Direktorat Konsuler Kemenlu untuk mendapatkan stiker legalisasi.</li>"
            "<li><strong>Tahap 3: Kedutaan/Konsulat Negara Tujuan</strong><br>Langkah terakhir adalah legalisasi di Kedutaan Besar atau Konsulat negara asing yang dituju di Indonesia.</li>"
            "</ul>"
            "<em>Catatan: Untuk negara-negara anggota Konvensi Apostille, prosesnya lebih sederhana dan hanya memerlukan sertifikat Apostille dari Kemenkumham.</em>"
        ),
        "follow_up": ["Berapa biaya legalisasi di Kemenlu?", "Apa itu Apostille?", "Dokumen apa saja yang bisa dilegalisasi?"]
    },
    {
        "pattern": r"(syarat|prosedur|cara|membuat).*(visa).*(diplomatik|dinas)",
        "priority": 9,
        "context": "visa diplomatik dan dinas",
        "answer": (
            "<strong>Persyaratan Visa Diplomatik dan Dinas</strong><br>"
            "Tentu, berikut adalah persyaratan umum untuk mengajukan permohonan Visa Diplomatik atau Visa Dinas ke Indonesia:<br><br>"
            "<ul>"
            "<li><strong>Permohonan Online:</strong> Wajib mengisi formulir dan mengunggah dokumen secara online melalui laman resmi di <a href='https://visa.kemlu.go.id/' target='_blank'>visa.kemlu.go.id</a>.</li>"
            "<li><strong>Paspor Asli:</strong> Menyerahkan paspor diplomatik atau dinas yang masih berlaku minimal 6 bulan saat kedatangan.</li>"
            "<li><strong>Nota Diplomatik:</strong> Melampirkan nota diplomatik resmi dari kementerian luar negeri atau perwakilan negara pengirim yang menjelaskan tujuan dan durasi penugasan.</li>"
            "<li><strong>Pas Foto:</strong> Menyerahkan 2 lembar pas foto berwarna terbaru (ukuran 4x6 cm) dengan latar belakang putih.</li>"
            "<li><strong>Tiket Perjalanan:</strong> Melampirkan salinan tiket atau rencana perjalanan (itinerary).</li>"
            "</ul>"
            "<em>Penting: Persyaratan dapat sedikit berbeda di setiap Perwakilan RI. Sangat disarankan untuk memeriksa situs web Perwakilan RI tempat Anda akan mengajukan visa.</em>"
        ),
        "follow_up": ["Berapa lama proses pembuatan visa diplomatik?", "Apakah ada biaya untuk visa diplomatik?"]
    },
    {
        "pattern": r"kekonsuleran|layanan konsuler|paspor|visa|legalisasi",
        "priority": 5, # Menurunkan prioritas agar keyword lebih spesifik didahulukan
        "context": "layanan konsuler umum",
        "answer": (
            '<strong>Layanan Kekonsuleran</strong><br><br>'
            'Layanan kekonsuleran mencakup berbagai hal penting bagi WNI di luar negeri dan WNA yang berkepentingan dengan Indonesia. Silakan pilih topik yang lebih spesifik di bawah ini atau ajukan pertanyaan langsung.<br><br>'
            '<strong>Beberapa Layanan Utama:</strong>'
            '<ul>'
            '<li><a href="https://kemlu.go.id/etc/pelayanan-paspor-diplomatik-dan-dinas" target="_blank">Paspor dan SPLP</a></li>'
            '<li><a href="https://kemlu.go.id/etc/informasi-kebijakan-visa-republik-indonesia" target="_blank">Visa (Diplomatik, Dinas, Kunjungan)</a></li>'
            '<li><a href="https://kemlu.go.id/etc/legalisasi-dokumen" target="_blank">Legalisasi Dokumen</a></li>'
            '<li><a href="https://peduliwni.kemlu.go.id/" target="_blank">Lapor Diri dan Pelindungan WNI</a></li>'
            '</ul>'
        ),
        "follow_up": ["Bagaimana cara perpanjang paspor?", "Apa syarat legalisasi dokumen?", "Bagaimana cara membuat visa kunjungan?"]
    },
    # ... (keyword lainnya tetap sama) ...
    {
        "pattern": r"pelindungan wni|wni bermasalah|bantuan wni",
        "priority": 8,
        "context": "pelindungan wni",
        "answer": (
            '<strong>Layanan Pelindungan WNI</strong><br><br>'
            '<strong>Tentang Layanan Pelindungan WNI:</strong>'
            '<ul>'
            '<li><a href="https://kemlu.go.id/etc/peraturan-pwni" target="_blank">Peraturan</a></li>'
            '<li><a href="https://kemlu.go.id/etc/maklumat-pelayanan-pwni" target="_blank">Maklumat Pelayanan</a></li>'
            '<li><a href="https://kemlu.go.id/etc/standar-pelayanan-pwni" target="_blank">Standar Pelayanan</a></li>'
            '<li><a href="https://kemlu.go.id/etc/video-pelayanan-pwni" target="_blank">Video Pelayanan</a></li>'
            '<li><a href="https://kemlu.go.id/etc/jadwal-pelayanan-kekonsuleran" target="_blank">Jadwal Pelayanan</a></li>'
            '<li><a href="https://kemlu.go.id/" target="_blank">Penilaian Kinerja</a></li>'
            '<li><a href="https://kemlu.go.id/etc/survei-kepuasan-masyarakat---pwni" target="_blank">Survei Kepuasan</a></li>'
            '<li><a href="https://kemlu.go.id/etc/faq-pwni" target="_blank">FAQ</a></li>'
            '<li><a href="https://kemlu.go.id/kontak" target="_blank">Pengaduan</a></li>'
            '<li><a href="https://peduliwni.kemlu.go.id/" target="_blank">Portal Peduli WNI</a></li>'
            '<li><a href="https://kemlu.go.id/pelindungan-wni-di-luar-negeri/safe-travel" target="_blank">Aplikasi Safe Travel</a></li>'
            '</ul>'
            '<strong>Produk Layanan Pelindungan WNI:</strong>'
            '<ul>'
            '<li><a href="https://kemlu.go.id/etc/pemberian-fasilitasi-pelindungan-wni" target="_blank">Pemberian Fasilitasi Pelindungan WNI</a></li>'
            '<li><a href="https://kemlu.go.id/etc/kampanye-penyadaran-publik" target="_blank">Kampanye Penyadaran Publik</a></li>'
            '<li><a href="https://kemlu.go.id/etc/penerimaan-permohonan-pelindungan-wni-di-luar-negeri" target="_blank">Penerimaan Permohonan Pelindungan WNI</a></li>'
            '<li><a href="https://peduliwni.kemlu.go.id/" target="_blank">Lapor Diri Online</a></li>'
            '</ul>'
        ),
        "follow_up": ["Bagaimana cara lapor diri online?", "Apa yang harus dilakukan jika paspor hilang?", "Bagaimana menghubungi KBRI terdekat dalam keadaan darurat?"]
    },
    {
        "pattern": r"fasilitas diplomatik|korps diplomatik",
        "priority": 7,
        "context": "fasilitas diplomatik",
        "answer": (
            '<strong>Layanan Fasilitas Diplomatik</strong><br><br>'
            '<strong>Tentang Layanan Fasilitas Diplomatik:</strong>'
            '<ul>'
            '<li><a href="https://kemlu.go.id/etc/buku-kebijakan-dan-pedoman-misi-luar-negeri" target="_blank">Buku Panduan</a></li>'
            '<li><a href="https://kemlu.go.id/etc/maklumat-pelayanan" target="_blank">Maklumat Pelayanan</a></li>'
            '<li><a href="https://kemlu.go.id/layanan/layanan-konsuler,-fasilitas-diplomatik-dan-pelindungan-wni/fasilitas-diplomatik" target="_blank">Standar Pelayanan</a></li>'
            '<li><a href="https://kemlu.go.id/etc/video-pelayanan-fasilitas-diplomatik" target="_blank">Video Pelayanan</a></li>'
            '<li><a href="https://kemlu.go.id/etc/jadwal-pelayanan-fasilitas-diplomatik" target="_blank">Jadwal Pelayanan</a></li>'
            '<li><a href="https://kemlu.go.id/etc/penilaian-kinerja-pelayanan-fasilitas-diplomatik" target="_blank">Penilaian Kinerja</a></li>'
            '<li><a href="https://kemlu.go.id/etc/survey-kepuasan" target="_blank">Survei Kepuasan</a></li>'
            '<li><a href="https://kemlu.go.id/layanan/layanan-konsuler,-fasilitas-diplomatik-dan-pelindungan-wni/fasilitas-diplomatik" target="_blank">FAQ</a></li>'
            '<li><a href="https://kemlu.go.id/kontak" target="_blank">Pengaduan</a></li>'
            '<li><a href="https://kemlu.go.id/etc/visi-misi-motto-dan-janji" target="_blank">Visi, Misi, Motto</a></li>'
            '</ul>'
            '<strong>Produk Layanan Fasilitas Diplomatik:</strong>'
            '<ul>'
            '<li><a href="https://kemlu.go.id/etc/fasilitas-kendaraan" target="_blank">Fasilitas Kendaraan</a></li>'
            '<li><a href="https://kemlu.go.id/etc/pendaftaran-kunjungan-regional-dan-fasilitas-akreditasi" target="_blank">Pendaftaran, Kunjungan Regional & Akreditasi</a></li>'
            '<li><a href="https://kemlu.go.id/etc/perizinan-bangunan" target="_blank">Perizinan Bangunan</a></li>'
            '<li><a href="https://kemlu.go.id/etc/senjata-api-dan-frekuensi-radio" target="_blank">Senjata Api dan Frekuensi Radio</a></li>'
            '<li><a href="https://kemlu.go.id/etc/pelayanan-fasilitasi-importasi-dan-eksportasi-barang-bagi-kantor-pna-dan-oi-di-indonesia" target="_blank">Fasilitasi Importasi & Eksportasi Barang</a></li>'
            '<li><a href="https://kemlu.go.id/etc/pelayanan-rekomendasi-pas-bandara-tahunan" target="_blank">Rekomendasi Pas Bandara Tahunan</a></li>'
            '<li><a href="https://kemlu.go.id/etc/pelayanan-penerbitan-id-card" target="_blank">Penerbitan ID Card</a></li>'
            '<li><a href="https://kemlu.go.id/etc/perpajakan" target="_blank">Perpajakan</a></li>'
            '</ul>'
        ),
        "follow_up": ["Bagaimana cara mengajukan ID Card diplomatik?", "Apa saja fasilitas untuk kendaraan korps diplomatik?", "Di mana saya bisa menemukan buku panduan?"]
    },
    {
        "pattern": r"kmiln|kartu masyarakat indonesia di luar negeri|diaspora card",
        "priority": 5,
        "context": "kmiln",
        "answer": 'Informasi lengkap tentang Kartu Masyarakat Indonesia di Luar Negeri (KMILN) atau Diaspora Card dapat diakses di <a href="https://kemlu.go.id/layanan/kartu-masyarakat-indonesia-di-luar-negeri" target="_blank">halaman KMILN Kemlu</a>.',
        "follow_up": ["Apa saja syarat membuat KMILN?", "Apa manfaat memiliki Diaspora Card?", "Bagaimana cara mendaftar?"]
    },
    {
        "pattern": r"pengaduan|lapor|sp4n",
        "priority": 5,
        "context": "pengaduan",
        "answer": 'Untuk pengaduan masyarakat umum, silakan gunakan layanan SP4N LAPOR!. Kunjungi <a href="https://kemlu.go.id/layanan/pengaduan-masyarakat" target="_blank">halaman pengaduan</a> untuk informasi dan akses layanan.',
        "follow_up": ["Bagaimana cara membuat laporan di SP4N?", "Apakah identitas pelapor dijamin kerahasiaannya?"]
    },
    {
        "pattern": r"ppid|informasi publik",
        "priority": 5,
        "context": "ppid",
        "answer": 'Layanan Pejabat Pengelola Informasi dan Dokumentasi (PPID) untuk permohonan informasi publik tersedia di <a href="https://kemlu.go.id/ppid" target="_blank">portal PPID Kemlu</a>.',
        "follow_up": ["Bagaimana cara mengajukan permohonan informasi publik?", "Informasi apa saja yang bisa saya minta melalui PPID?", "Berapa lama proses permohonan informasi?"]
    },
    {
        "pattern": r"csca|country signing certificate authority|sertifikat paspor",
        "priority": 4,
        "context": "csca",
        "answer": 'Informasi mengenai Country Signing Certificate Authority (CSCA) Indonesia untuk validasi e-paspor dapat diakses di <a href="https://kemlu.go.id/layanan/layanan-konsuler-fasilitas-diplomatik-dan-pelindungan-wni/country-signing-certificate-authority-csca" target="_blank">halaman CSCA Kemlu</a>.',
        "follow_up": ["Apa itu CSCA?", "Bagaimana cara mengunduh sertifikat CSCA?"]
    },
    {
        "pattern": r"jdih|jaringan dokumentasi|informasi hukum",
        "priority": 4,
        "context": "jdih",
        "answer": 'Informasi mengenai Jaringan Dokumentasi dan Informasi Hukum (JDIH) dapat diakses di <a href="https://kemlu.go.id/layanan/jaringan-dokumentasi-dan-informasi-hukum" target="_blank">halaman JDIH Kemlu</a>.',
        "follow_up": ["Apa saja produk hukum yang tersedia?", "Bagaimana cara mencari peraturan?"]
    },
    {
        "pattern": r"ormas asing|pendaftaran ormas|ngo asing",
        "priority": 4,
        "context": "ormas asing",
        "answer": 'Prosedur dan informasi pendaftaran Organisasi Kemasyarakatan (Ormas) Asing di Indonesia tersedia di <a href="https://kemlu.go.id/layanan/pendaftaran-ormas-asing-indonesia" target="_blank">halaman pendaftaran Ormas Asing</a>.',
        "follow_up": ["Apa saja syarat pendaftaran ormas asing?", "Berapa lama prosesnya?"]
    },
    {
        "pattern": r"pelayanan media|media|peliputan|pers",
        "priority": 4,
        "context": "pelayanan media",
        "answer": 'Untuk fasilitasi peliputan kegiatan Kemlu dan Perwakilan RI oleh media, silakan kunjungi halaman <a href="https://kemlu.go.id/layanan/pelayanan-media" target="_blank">Pelayanan Media</a> di situs resmi Kemlu.',
        "follow_up": ["Bagaimana prosedur akreditasi media asing?", "Di mana saya bisa mendapatkan siaran pers resmi?", "Siapa narahubung untuk media?"]
    },
    {
        "pattern": r"rogatory|rogatori|bantuan hukum internasional",
        "priority": 4,
        "context": "rogatory",
        "answer": 'Layanan Rogatory Online untuk permintaan bantuan hukum internasional dapat diakses melalui <a href="https://kemlu.go.id/layanan/rogatory-online" target="_blank">halaman Rogatory Online</a>.',
        "follow_up": ["Bagaimana prosedur pengajuan rogatori?", "Siapa yang bisa mengajukan?"]
    },
    {
        "pattern": r"treaty database|database perjanjian|perjanjian internasional",
        "priority": 4,
        "context": "treaty database",
        "answer": 'Database Perjanjian Internasional yang dimiliki Indonesia dapat ditelusuri di <a href="https://kemlu.go.id/layanan/treaty-database" target="_blank">Treaty Database Kemlu</a>.',
        "follow_up": ["Bagaimana cara mencari perjanjian?", "Perjanjian apa saja yang ada?"]
    },
    {
        "pattern": r"ukpbj|pengadaan barang jasa|lelang|tender kemlu",
        "priority": 4,
        "context": "ukpbj",
        "answer": 'Informasi mengenai Unit Kerja Pengadaan Barang/Jasa (UKPBJ) Kementerian Luar Negeri dapat ditemukan di <a href="https://kemlu.go.id/layanan/unit-kerja-pengadaan-barangjasa-ukpbj" target="_blank">halaman UKPBJ</a>.',
        "follow_up": ["Bagaimana cara mengikuti tender?", "Di mana melihat pengumuman lelang terbaru?"]
    },
    {
        "pattern": r"karir|lowongan kerja kemlu|rekrutmen asn",
        "priority": 3,
        "context": "karir",
        "answer": 'Informasi mengenai peluang karir dan rekrutmen di Kementerian Luar Negeri tersedia di <a href="https://kemlu.go.id/karir" target="_blank">halaman Karir</a>.',
        "follow_up": ["Kapan pendaftaran diplomat dibuka?", "Apa saja persyaratan untuk menjadi diplomat?", "Bagaimana proses seleksinya?"]
    },
    {
        "pattern": r"perwakilan ri|daftar perwakilan",
        "priority": 3,
        "context": "perwakilan ri",
        "answer": 'Daftar lengkap Perwakilan Republik Indonesia di luar negeri (KBRI, KJRI, KRI, dan PTRI) dapat diakses di <a href="https://kemlu.go.id/perwakilan" target="_blank">halaman Perwakilan</a>.',
        "follow_up": ["Di mana alamat KBRI terdekat?", "Bagaimana cara menghubungi Konsulat Jenderal?"]
    },
    {
        "pattern": r"perwakilan asing|kedutaan asing|konsulat asing",
        "priority": 3,
        "context": "perwakilan asing",
        "answer": 'Daftar Perwakilan Diplomatik dan Konsuler Asing di Indonesia dapat ditemukan di <a href="https://kemlu.go.id/layanan/layanan-konsuler-fasilitas-diplomatik-dan-pelindungan-wni/daftar-perwakilan-diplomatik-dan-konsuler-asing" target="_blank">halaman ini</a>.',
        "follow_up": ["Di mana alamat kedutaan besar negara sahabat?", "Bagaimana cara menghubungi konsulat asing?"]
    },
    {
        "pattern": r"berita|artikel terkini",
        "priority": 2,
        "context": "berita",
        "answer": 'Berita dan siaran pers terbaru dari Kementerian Luar Negeri dapat diakses di <a href="https://kemlu.go.id/berita" target="_blank">halaman Berita</a>.',
        "follow_up": ["Di mana saya bisa menemukan siaran pers?", "Bagaimana cara berlangganan berita Kemlu?"]
    },
    {
        "pattern": r"kebijakan luar negeri|polugri|kebijakan",
        "priority": 2,
        "context": "kebijakan luar negeri",
        "answer": '<strong>Kebijakan Luar Negeri Indonesia</strong><br>Informasi mengenai kebijakan luar negeri Indonesia dapat diakses melalui tautan berikut:<ul>'
                  '<li><a href="https://kemlu.go.id/kebijakan/landasan-visi-dan-misi-polugri" target="_blank">Landasan, Visi dan Misi Polugri</a></li>'
                  '<li><a href="https://kemlu.go.id/kebijakan/asean" target="_blank">ASEAN</a></li>'
                  '<li><a href="https://kemlu.go.id/kebijakan/kerja-sama-bilateral" target="_blank">Kerja Sama Bilateral</a></li>'
                  '<li><a href="https://kemlu.go.id/kebijakan/kerja-sama-regional" target="_blank">Kerja Sama Regional</a></li>'
                  '<li><a href="https://kemlu.go.id/kebijakan/kerja-sama-multilateral" target="_blank">Kerja Sama Multilateral</a></li>'
                  '<li><a href="https://kemlu.go.id/kebijakan/diplomasi-ekonomi" target="_blank">Diplomasi Ekonomi</a></li>'
                  '<li><a href="https://kemlu.go.id/kebijakan/organisasi-internasional" target="_blank">Organisasi Internasional</a></li>'
                  '<li><a href="https://kemlu.go.id/kebijakan/pengarusutamaan-gender" target="_blank">Pengarusutamaan Gender</a></li>'
                  '<li><a href="https://kemlu.go.id/kebijakan/isu-khusus" target="_blank">Isu Khusus</a></li>'
                  '<li><a href="https://kemlu.go.id/kebijakan/reformasi-birokrasi-kemlu" target="_blank">Reformasi Birokrasi Kemlu</a></li></ul>',
        "follow_up": ["Apa fokus utama diplomasi Indonesia?", "Bagaimana kerja sama Indonesia dengan negara lain?", "Di mana saya bisa membaca tentang reformasi birokrasi Kemlu?"]
    },
    {
        "pattern": r"kinerja kementerian|laporan kinerja|akip",
        "priority": 2,
        "context": "kinerja kementerian",
        "answer": '<strong>Kinerja Kementerian Luar Negeri</strong><br>Laporan kinerja Kementerian Luar Negeri, termasuk Akuntabilitas Kinerja Instansi Pemerintah (AKIP), dapat diakses melalui tautan berikut:<ul>'
                  '<li><a href="https://kemlu.go.id/kinerja/kinerja-kementerian-luar-negeri" target="_blank">Kinerja Kementerian Luar Negeri (Umum)</a></li>'
                  '<li><strong>Laporan AKIP per Unit:</strong><ul>'
                  '<li><a href="https://kemlu.go.id/kinerja/akip/kementerian-luar-negeri" target="_blank">Kementerian Luar Negeri</a></li>'
                  '<li><a href="https://kemlu.go.id/kinerja/akip/sekretariat-jenderal" target="_blank">Sekretariat Jenderal</a></li>'
                  '<li><a href="https://kemlu.go.id/kinerja/akip/direktorat-jenderal-amerop" target="_blank">Direktorat Jenderal AMEROP</a></li>'
                  '<li><a href="https://kemlu.go.id/kinerja/akip/direktorat-jenderal-aspasaf" target="_blank">Direktorat Jenderal ASPASAF</a></li>'
                  '<li><a href="https://kemlu.go.id/kinerja/akip/direktorat-jenderal-kerjasama-asean" target="_blank">Direktorat Jenderal Kerjasama ASEAN</a></li>'
                  '<li><a href="https://kemlu.go.id/kinerja/akip/direktorat-jenderal-kerjasama-multilateral" target="_blank">Direktorat Jenderal Kerjasama Multilateral</a></li>'
                  '<li><a href="https://kemlu.go.id/kinerja/akip/direktorat-jenderal-informasi-dan-diplomasi-publik" target="_blank">Direktorat Jenderal Informasi dan Diplomasi Publik</a></li>'
                  '<li><a href="https://kemlu.go.id/kinerja/akip/direktorat-jenderal-hukum-dan-perjanjian-internasional" target="_blank">Direktorat Jenderal Hukum dan Perjanjian Internasional</a></li>'
                  '<li><a href="https://kemlu.go.id/kinerja/akip/direktorat-jenderal-protokol-dan-konsuler" target="_blank">Direktorat Jenderal Protokol dan Konsuler</a></li>'
                  '<li><a href="https://kemlu.go.id/kinerja/akip/inspektorat-jenderal" target="_blank">Inspektorat Jenderal</a></li>'
                  '<li><a href="https://kemlu.go.id/kinerja/akip/badan-strategi-kebijakan-luar-negeri" target="_blank">Badan Strategi Kebijakan Luar Negeri</a></li>'
                  '<li><a href="https://kemlu.go.id/kinerja/akip/pusat-pendidikan-dan-pelatihan" target="_blank">Pusat Pendidikan dan Pelatihan</a></li>'
                  '</ul></li></ul>',
        "follow_up": ["Bagaimana cara mengunduh laporan AKIP?", "Apa saja capaian kinerja Kemlu tahun lalu?"]
    },
    {
        "pattern": r"publikasi|buku|jurnal|pidato|siaran pers",
        "priority": 2,
        "context": "publikasi",
        "answer": '<strong>Publikasi Kementerian Luar Negeri</strong><br>Berbagai publikasi resmi dapat diakses melalui tautan berikut:<ul>'
                  '<li><a href="https://kemlu.go.id/publikasi/agenda" target="_blank">Agenda</a></li>'
                  '<li><strong>Buku:</strong><ul>'
                  '<li><a href="https://kemlu.go.id/publikasi/buku/buku-diplomasi-ekonomi-kreatif" target="_blank">Buku Diplomasi Ekonomi Kreatif</a></li>'
                  '<li><a href="https://kemlu.go.id/publikasi/buku/buku-diplomasi-indonesia" target="_blank">Buku Diplomasi Indonesia</a></li>'
                  '</ul></li>'
                  '<li><a href="https://kemlu.go.id/publikasi/galeri-diplomasi" target="_blank">Galeri Diplomasi</a></li>'
                  '<li><strong>Jurnal:</strong><ul>'
                  '<li><a href="https://kemlu.go.id/publikasi/jurnal/jurnal-hubungan-luar-negeri" target="_blank">Jurnal Hubungan Luar Negeri</a></li>'
                  '<li><a href="https://kemlu.go.id/publikasi/jurnal/opinio-juris" target="_blank">Opinio Juris</a></li>'
                  '<li><a href="https://kemlu.go.id/publikasi/jurnal/treaty-journal" target="_blank">Treaty Journal</a></li>'
                  '</ul></li>'
                  '<li><strong>Kajian:</strong><ul>'
                  '<li><a href="https://kemlu.go.id/publikasi/kajian/dashboard" target="_blank">Dashboard</a></li>'
                  '<li><a href="https://kemlu.go.id/publikasi/kajian/policy-brief-" target="_blank">Policy Brief</a></li>'
                  '<li>Pusat Strategi Kebijakan: <a href="https://kemlu.go.id/publikasi/kajian/pusat-strategi-kebijakan-isu-khusus-dan-analisis-data" target="_blank">Isu Khusus</a>, <a href="https://kemlu.go.id/publikasi/kajian/pusat-strategi-kebijakan-kawasan-amerika-dan-eropa" target="_blank">Amerop</a>, <a href="https://kemlu.go.id/publikasi/kajian/pusat-strategi-kebijakan-kawasan-asia-pasifik-dan-afrika" target="_blank">Aspasaf</a>, <a href="https://kemlu.go.id/publikasi/kajian/pusat-strategi-kebijakan-multilateral" target="_blank">Multilateral</a></li>'
                  '<li><a href="https://kemlu.go.id/publikasi/kajian/sekretariat-badan-strategi-kebijakan-luar-negeri" target="_blank">Sekretariat BSKLN</a></li>'
                  '</ul></li>'
                  '<li><a href="https://kemlu.go.id/publikasi/majalah" target="_blank">Majalah</a></li>'
                  '<li><strong>Pidato:</strong><ul>'
                  '<li><a href="https://kemlu.go.id/publikasi/pidato/pidato-presiden" target="_blank">Pidato Presiden</a></li>'
                  '<li><a href="https://kemlu.go.id/publikasi/pidato/pidato-menteri" target="_blank">Pidato Menteri</a></li>'
                  '<li><a href="https://kemlu.go.id/publikasi/pidato/pidato-lainnya" target="_blank">Pidato Lainnya</a></li>'
                  '</ul></li>'
                  '<li><a href="https://kemlu.go.id/publikasi/siaran-pers" target="_blank">Siaran Pers</a></li>'
                  '<li><a href="https://kemlu.go.id/publikasi/tabloid-diplomasi" target="_blank">Tabloid Diplomasi</a></li>'
                  '</ul>',
        "follow_up": ["Di mana saya bisa mengunduh buku tentang diplomasi?", "Apakah transkrip pidato Menteri Luar Negeri tersedia?", "Bagaimana cara mengakses jurnal ilmiah Kemlu?"]
    },
    {
        "pattern": r"daftar joint statement|pernyataan bersama",
        "priority": 2,
        "context": "joint statement",
        "answer": 'Daftar pernyataan bersama (Joint Statement) dapat ditemukan di <a href="https://kemlu.go.id/daftar-joint-statement" target="_blank">halaman Joint Statement</a>.',
        "follow_up": ["Apa itu joint statement?", "Bagaimana cara mencari pernyataan bersama dengan negara tertentu?"]
    },
    {
        "pattern": r"faq|pertanyaan umum",
        "priority": 1,
        "context": "faq",
        "answer": 'Jawaban untuk pertanyaan yang sering diajukan (FAQ) dapat ditemukan di <a href="https://kemlu.go.id/faq" target="_blank">halaman FAQ Kemlu</a>.',
        "follow_up": ["Apakah ada FAQ untuk layanan paspor?", "Di mana saya bisa bertanya jika jawaban tidak ada di FAQ?"]
    },
    {
        "pattern": r"kontak|hubungi kemlu",
        "priority": 1,
        "context": "kontak kemlu",
        "answer": 'Informasi kontak Kementerian Luar Negeri dapat ditemukan di <a href="https://kemlu.go.id/kontak" target="_blank">halaman Kontak</a>.',
        "follow_up": ["Apa alamat email resmi Kemlu?", "Berapa nomor telepon yang bisa dihubungi?"]
    },
    {
        "pattern": r"media sosial|sosmed",
        "priority": 1,
        "context": "media sosial",
        "answer": 'Ikuti akun media sosial resmi Kementerian Luar Negeri untuk mendapatkan informasi terbaru:<ul><li><strong>Instagram:</strong> <a href="https://www.instagram.com/kemlu_ri/" target="_blank">@kemlu_ri</a></li><li><strong>X (Twitter):</strong> <a href="https://x.com/Kemlu_RI" target="_blank">@Kemlu_RI</a></li><li><strong>Facebook:</strong> <a href="https://id-id.facebook.com/Kemlu.RI/" target="_blank">Kemlu.RI</a></li><li><strong>YouTube:</strong> <a href="https://www.youtube.com/channel/UCPvFP6lS5EauoyT3GyPtfwA" target="_blank">MoFA Indonesia</a></li></ul>',
        "follow_up": ["Apakah Kemlu punya akun TikTok?", "Bagaimana cara mendapatkan update dari media sosial?"]
    },
    {
        "pattern": r"peta situs|sitemap",
        "priority": 1,
        "context": "peta situs",
        "answer": 'Untuk melihat struktur lengkap situs web Kementerian Luar Negeri, silakan kunjungi <a href="https://kemlu.go.id/peta-situs" target="_blank">Peta Situs</a>.',
        "follow_up": ["Bagaimana cara mencari informasi spesifik di situs Kemlu?"]
    },
    {
        "pattern": r"tautan|link terkait",
        "priority": 1,
        "context": "tautan",
        "answer": 'Daftar tautan atau pranala terkait institusi pemerintah dan organisasi lainnya dapat ditemukan di <a href="https://kemlu.go.id/tautan" target="_blank">halaman Tautan</a>.',
        "follow_up": ["Apakah ada link ke situs kementerian lain?", "Di mana link ke portal Peduli WNI?"]
    },
    {
        "pattern": r"layanan|daftar layanan",
        "priority": 1,
        "context": "layanan kemlu",
        "answer": "<strong>Daftar Layanan Kementerian Luar Negeri</strong><br>Berikut adalah beberapa layanan utama yang tersedia melalui situs resmi Kementerian Luar Negeri:"
                  "<ul>"
                  "<li>Layanan Konsuler (Paspor, Visa, Legalisasi)</li>"
                  "<li>Pelindungan Warga Negara Indonesia (WNI)</li>"
                  "<li>Layanan Pengaduan Masyarakat (SP4N LAPOR!)</li>"
                  "<li>Permohonan Informasi Publik (PPID)</li>"
                  "<li>Pendaftaran Kartu Masyarakat Indonesia di Luar Negeri (KMILN)</li>"
                  "<li>Bantuan Hukum Internasional (Rogatori)</li>"
                  "<li>Informasi Jaringan Dokumentasi dan Informasi Hukum (JDIH)</li>"
                  "<li>Database Perjanjian Internasional</li>"
                  "<li>Layanan Media dan Pers</li>"
                  "<li>Fasilitas Diplomatik</li>"
                  "<li>Pendaftaran Ormas Asing</li>"
                  "<li>Pengadaan Barang/Jasa (UKPBJ)</li>"
                  "<li>Informasi Karir</li>"
                  "</ul>"
                  "Anda dapat menanyakan layanan spesifik yang Anda butuhkan untuk informasi lebih detail.",
        "follow_up": ["Bagaimana cara membuat paspor di luar negeri?", "Apa yang harus saya lakukan jika dalam keadaan darurat di luar negeri?", "Bagaimana cara mengajukan pengaduan?"]
    },
]

KEYWORDS_EN = [
    {
        "pattern": r"career|job vacancy|recruitment",
        "priority": 5,
        "context": "career",
        "answer": 'Information about career opportunities and recruitment at the Ministry of Foreign Affairs is available on the <a href="https://kemlu.go.id/karir" target="_blank">Career page</a>.',
        "follow_up": ["When does registration for diplomats open?", "What are the requirements to become a diplomat?", "What is the selection process like?"]
    },
    {
        "pattern": r"complaint|report issue|sp4n",
        "priority": 5,
        "context": "complaint",
        "answer": 'For public complaints, please use the SP4N LAPOR! service. Visit the <a href="https://kemlu.go.id/layanan/pengaduan-masyarakat" target="_blank">complaints page</a> for information and access to these services.',
        "follow_up": ["How do I file a report on SP4N?", "Is the reporter's identity kept confidential?"]
    },
    {
        "pattern": r"consular services|consular affairs|passport|visa|legalization",
        "priority": 8,
        "context": "consular services",
        "answer": 'Information on consular services can be found on the <a href="https://kemlu.go.id/layanan/layanan-konsuler-fasilitas-diplomatik-dan-pelindungan-wni/kekonsuleran" target="_blank">Ministry\'s Consular Affairs page</a>.',
        "follow_up": ["How do I apply for a passport abroad?", "What are the requirements for document legalization?", "How do I register the birth of a child?"]
    },
    {
        "pattern": r"contact|contact us",
        "priority": 1,
        "context": "contact",
        "answer": 'Contact information for the Ministry of Foreign Affairs can be found on the <a href="https://kemlu.go.id/kontak" target="_blank">Contact page</a>.',
        "follow_up": ["What is the official email address of the Ministry?", "What is the contact phone number?"]
    },
    {
        "pattern": r"csca|country signing certificate authority|passport certificate",
        "priority": 4,
        "context": "csca",
        "answer": 'Information about Indonesia\'s Country Signing Certificate Authority (CSCA) for e-passport validation can be accessed on the <a href="https://kemlu.go.id/layanan/layanan-konsuler-fasilitas-diplomatik-dan-pelindungan-wni/country-signing-certificate-authority-csca" target="_blank">Ministry\'s CSCA page</a>.',
        "follow_up": ["What is CSCA?", "How to download the CSCA certificate?"]
    },
    {
        "pattern": r"diplomatic facilities|diplomatic corps",
        "priority": 7,
        "context": "diplomatic facilities",
        "answer": "Services related to diplomatic facilities for foreign missions and international organizations can be accessed on the <a href='https://kemlu.go.id/layanan/layanan-konsuler-fasilitas-diplomatik-dan-pelindungan-wni/fasilitas-diplomatik' target='_blank'>Diplomatic Facilities page</a>.",
        "follow_up": ["Who can use this service?", "How to access the diplomatic handbook?"]
    },
    {
        "pattern": r"faq|frequently asked questions",
        "priority": 1,
        "context": "faq",
        "answer": 'Answers to frequently asked questions (FAQ) can be found on the <a href="https://kemlu.go.id/faq" target="_blank">Ministry\'s FAQ page</a>.',
        "follow_up": ["Is there an FAQ for passport services?", "Where can I ask if my question is not in the FAQ?"]
    },
    {
        "pattern": r"foreign mission|foreign embassy|foreign consulate",
        "priority": 3,
        "context": "foreign mission",
        "answer": 'The list of Foreign Diplomatic and Consular Missions in Indonesia can be found on <a href="https://kemlu.go.id/layanan/layanan-konsuler-fasilitas-diplomatik-dan-pelindungan-wni/daftar-perwakilan-diplomatik-dan-konsuler-asing" target="_blank">this page</a>.',
        "follow_up": ["Where is the embassy of a foreign country?", "How do I contact a foreign consulate?"]
    },
    {
        "pattern": r"foreign ngo|foreign organization registration|international ngo",
        "priority": 4,
        "context": "foreign ngo",
        "answer": 'Procedures and information for registering Foreign Community Organizations in Indonesia are available on the <a href="https://kemlu.go.id/layanan/pendaftaran-ormas-asing-indonesia" target="_blank">Foreign Organization registration page</a>.',
        "follow_up": ["What are the registration requirements for foreign NGOs?", "How long is the process?"]
    },
    {
        "pattern": r"foreign policy",
        "priority": 2,
        "context": "foreign policy",
        "answer": 'General information about Indonesia\'s foreign policy, including its foundation, vision, and mission, can be accessed on the <a href="https://kemlu.go.id/kebijakan/landasan-visi-dan-misi-polugri" target="_blank">Policy page</a>. This page also covers bilateral, regional, and multilateral cooperation.',
        "follow_up": ["What are the main focuses of Indonesian diplomacy today?", "What is Indonesia's policy on global issues?", "Where can I read about cooperation with other countries?"]
    },
    {
        "pattern": r"indonesian missions|list of missions|embassies list",
        "priority": 3,
        "context": "indonesian missions",
        "answer": 'The complete list of the Republic of Indonesia\'s Missions abroad (Embassies, Consulate Generals, Consulates, and Permanent Missions) can be accessed on the <a href="https://kemlu.go.id/perwakilan" target="_blank">Missions page</a>.',
        "follow_up": ["Where is the nearest Indonesian Embassy?", "How do I contact the Consulate General?"]
    },
    {
        "pattern": r"jdih|legal documentation|legal information network",
        "priority": 4,
        "context": "jdih",
        "answer": 'Information about the Legal Documentation and Information Network (JDIH) can be accessed on the <a href="https://kemlu.go.id/layanan/jaringan-dokumentasi-dan-informasi-hukum" target="_blank">Ministry\'s JDIH page</a>.',
        "follow_up": ["What legal products are available?", "How do I search for regulations?"]
    },
    {
        "pattern": r"joint statement|list of joint statements",
        "priority": 2,
        "context": "joint statement",
        "answer": 'The list of joint statements can be found on the <a href="https://kemlu.go.id/daftar-joint-statement" target="_blank">Joint Statement page</a>.',
        "follow_up": ["What is a joint statement?", "How can I find a joint statement with a specific country?"]
    },
    {
        "pattern": r"kmiln|card for indonesian diaspora|diaspora card",
        "priority": 5,
        "context": "kmiln",
        "answer": 'Complete information about the Card for Indonesian Diaspora (KMILN) or Diaspora Card is available at <a href="https://kemlu.go.id/layanan/kartu-masyarakat-indonesia-di-luar-negeri" target="_blank">the Ministry\'s KMILN page</a>.',
        "follow_up": ["What are the requirements for the KMILN card?", "What are the benefits of having a Diaspora Card?", "How do I apply?"]
    },
    {
        "pattern": r"links|related links",
        "priority": 1,
        "context": "links",
        "answer": 'A list of related links to government institutions and other organizations can be found on the <a href="https://kemlu.go.id/tautan" target="_blank">Links page</a>.',
        "follow_up": ["Is there a link to other ministry websites?", "Where is the link to the Peduli WNI portal?"]
    },
    {
        "pattern": r"media services|press|media coverage",
        "priority": 4,
        "context": "media services",
        "answer": 'For facilitation of media coverage of Ministry and Mission activities, please visit the <a href="https://kemlu.go.id/layanan/pelayanan-media" target="_blank">Media Services</a> page on the official website.',
        "follow_up": ["What is the accreditation procedure for foreign media?", "Where can I find official press releases?", "Who is the contact person for the press?"]
    },
    {
        "pattern": r"ministry performance|performance report|akip",
        "priority": 2,
        "context": "ministry performance",
        "answer": 'Performance reports of the Ministry of Foreign Affairs, including the Government Agency Performance Accountability (AKIP) for each work unit, can be accessed through the <a href="https://kemlu.go.id/kinerja/kinerja-kementerian-luar-negeri" target="_blank">Performance portal</a>.',
        "follow_up": ["How do I download the AKIP report?", "What were the Ministry's performance achievements last year?"]
    },
    {
        "pattern": r"news|latest articles|press release",
        "priority": 2,
        "context": "news",
        "answer": 'The latest news and press releases from the Ministry of Foreign Affairs can be accessed on the <a href="https://kemlu.go.id/berita" target="_blank">News page</a>.',
        "follow_up": ["Where can I find press releases?", "How can I subscribe to the Ministry's news?"]
    },
    {
        "pattern": r"procurement|goods and services procurement|tender|bidding",
        "priority": 4,
        "context": "procurement",
        "answer": 'Information about the Goods/Services Procurement Unit (UKPBJ) of the Ministry of Foreign Affairs can be found on the <a href="https://kemlu.go.id/layanan/unit-kerja-pengadaan-barangjasa-ukpbj" target="_blank">UKPBJ page</a>.',
        "follow_up": ["How to participate in a tender?", "Where can I see the latest tender announcements?"]
    },
    {
        "pattern": r"protection|citizen protection|emergency assistance",
        "priority": 10,
        "context": "citizen protection",
        "answer": 'Services for the protection of Indonesian citizens are available at the <a href="https://kemlu.go.id/layanan/layanan-konsuler-fasilitas-diplomatik-dan-pelindungan-wni/pelindungan-wni" target="_blank">Citizen Protection portal</a>. For emergencies, contact the nearest Indonesian Mission immediately.',
        "follow_up": ["Where is the nearest Indonesian Mission?", "What should I do if I lose my passport abroad?", "How can I contact the emergency hotline?"]
    },
    {
        "pattern": r"ppid|public information",
        "priority": 5,
        "context": "ppid",
        "answer": 'The Information and Documentation Management Officer (PPID) service for public information requests is available at the <a href="https://kemlu.go.id/ppid" target="_blank">Ministry\'s PPID portal</a>.',
        "follow_up": ["How do I submit a public information request?", "What information can I request through PPID?", "How long does the information request process take?"]
    },
    {
        "pattern": r"publications|books|journals|speeches|press releases",
        "priority": 2,
        "context": "publications",
        "answer": 'Various official publications from the Ministry of Foreign Affairs such as books, journals, studies, speeches, and press releases can be accessed through the <a href="https://kemlu.go.id/publikasi/agenda" target="_blank">Publications portal</a>.',
        "follow_up": ["Where can I download books on Indonesian diplomacy?", "Are transcripts of the Foreign Minister's speeches available?", "How can I access the Ministry's scientific journals?"]
    },
    {
        "pattern": r"rogatory|letters rogatory|international legal assistance",
        "priority": 4,
        "context": "rogatory",
        "answer": 'The Online Rogatory service for international legal assistance requests can be accessed through the <a href="https://kemlu.go.id/layanan/rogatory-online" target="_blank">Online Rogatory page</a>.',
        "follow_up": ["What is the procedure for a rogatory request?", "Who can submit a request?"]
    },
    {
        "pattern": r"services|list of services",
        "priority": 1,
        "context": "services",
        "answer": "<strong>List of Ministry of Foreign Affairs Services</strong><br>Here are some of the main services available through the official Ministry of Foreign Affairs website:"
                  "<ul>"
                  "<li>Consular Services (Passport, Visa, Legalization)</li>"
                  "<li>Protection for Indonesian Citizens Abroad</li>"
                  "<li>Public Complaint Services (SP4N LAPOR!)</li>"
                  "<li>Public Information Requests (PPID)</li>"
                  "<li>Card for Indonesian Diaspora (KMILN) Registration</li>"
                  "<li>International Legal Assistance (Rogatory)</li>"
                  "<li>Legal Documentation and Information Network (JDIH)</li>"
                  "<li>International Treaty Database</li>"
                  "<li>Media and Press Services</li>"
                  "<li>Diplomatic Facilities</li>"
                  "<li>Foreign NGO Registration</li>"
                  "<li>Goods/Services Procurement (UKPBJ)</li>"
                  "<li>Career Information</li>"
                  "</ul>"
                  "You can ask about the specific service you need for more detailed information.",
        "follow_up": ["How do I apply for a passport abroad?", "What should I do in an emergency situation abroad?", "How do I file a complaint?"]
    },
    {
        "pattern": r"sitemap",
        "priority": 1,
        "context": "sitemap",
        "answer": 'To see the complete structure of the Ministry of Foreign Affairs website, please visit the <a href="https://kemlu.go.id/peta-situs" target="_blank">Sitemap</a>.',
        "follow_up": ["How do I find specific information on the Ministry's website?"]
    },
    {
        "pattern": r"social media",
        "priority": 1,
        "context": "social media",
        "answer": 'Follow the official social media accounts of the Ministry of Foreign Affairs for the latest updates:<ul><li><strong>Instagram:</strong> <a href="https://www.instagram.com/kemlu_ri/" target="_blank">@kemlu_ri</a></li><li><strong>X (Twitter):</strong> <a href="https://x.com/Kemlu_RI" target="_blank">@Kemlu_RI</a></li><li><strong>Facebook:</strong> <a href="https://id-id.facebook.com/Kemlu.RI/" target="_blank">Kemlu.RI</a></li><li><strong>YouTube:</strong> <a href="https://www.youtube.com/channel/UCPvFP6lS5EauoyT3GyPtfwA" target="_blank">MoFA Indonesia</a></li></ul>',
        "follow_up": ["Does the Ministry have a TikTok account?", "How can I get updates from social media?"]
    },
    {
        "pattern": r"treaty database|international agreements|treaties",
        "priority": 2,
        "context": "treaty database",
        "answer": 'Indonesia\'s International Agreement Database can be searched at the <a href="https://kemlu.go.id/layanan/treaty-database" target="_blank">Ministry\'s Treaty Database</a>.',
        "follow_up": ["How do I search for a treaty?", "What treaties are available?"]
    }
]


# --- REPRESENTATIVE OFFICE DATA ---
PERWAKILAN_DATA = {
    "Asia": {
        "afghanistan": {
            "name": "KBRI Kabul",
            "aliases": [],
            "link": "https://kemlu.go.id/kabul",
            "address": "Malalai Watt, Shah-re-Naw, Kabul, Afghanistan",
            "google_maps_link": "https://www.google.com/maps/search/?api=1&query=Malalai+Watt%2C+Shah-re-Naw%2C+Kabul%2C+Afghanistan"
        },
        "arab saudi": {
            "name": "KBRI Riyadh",
            "aliases": ["saudi arabia"],
            "link": "https://kemlu.go.id/riyadh",
            "address": "Diplomatic Quarter, P.O. Box 94343 - Riyadh 11693, Arab Saudi",
            "google_maps_link": "https://www.google.com/maps/search/?api=1&query=Diplomatic+Quarter%2C+Riyadh%2C+Saudi+Arabia"
        },
        "azerbaijan": {
            "name": "KBRI Baku",
            "aliases": [],
            "link": "https://kemlu.go.id/baku",
            "address": "4 Azer Aliyev, Nasimi District, Baku City, 1022, Azerbaijan",
            "google_maps_link": "https://www.google.com/maps/search/?api=1&query=4+Azer+Aliyev%2C+Nasimi+District%2C+Baku+City%2C+1022%2C+Azerbaijan"
        },
        "bahrain": {
            "name": "KBRI Manama",
            "aliases": [],
            "link": "https://kemlu.go.id/manama",
            "address": "Villa 2113, Road 2432, Block 324, Juffair, Manama, Bahrain",
            "google_maps_link": "https://www.google.com/maps/search/?api=1&query=Villa+2113%2C+Road+2432%2C+Block+324%2C+Juffair%2C+Manama%2C+Bahrain"
        },
        "bangladesh": {
            "name": "KBRI Dhaka",
            "aliases": [],
            "link": "https://kemlu.go.id/dhaka",
            "address": "Road No. 53, Plot No. 14, Gulshan-2 Dhaka-1212, Bangladesh",
            "google_maps_link": "https://www.google.com/maps/search/?api=1&query=Road+No.+53%2C+Plot+No.+14%2C+Gulshan-2+Dhaka-1212%2C+Bangladesh"
        },
        "brunei darussalam": {
            "name": "KBRI Bandar Seri Begawan",
            "aliases": ["brunei"],
            "link": "https://kemlu.go.id/bandarseribegawan",
            "address": "Simpang 336, Diplomatic Enclave, Bandar Seri Begawan, Brunei",
            "google_maps_link": "https://www.google.com/maps/search/?api=1&query=Simpang+336%2C+Diplomatic+Enclave%2C+Bandar+Seri+Begawan%2C+Brunei"
        },
        "china": {
            "name": "KBRI Beijing",
            "aliases": ["tiongkok"],
            "link": "https://kemlu.go.id/beijing",
            "address": "Dongzhimen Wai Da Jie No. 4 Chaoyang District, Bejing 100600, P.R Tiongkok",
            "google_maps_link": "https://www.google.com/maps/search/?api=1&query=Dongzhimen+Wai+Da+Jie+No.+4+Chaoyang+District%2C+Bejing+100600"
        },
        "filipina": {
            "name": "KBRI Manila",
            "aliases": ["philippines"],
            "link": "https://kemlu.go.id/manila",
            "address": "185 Salcedo St, Legaspi Village, Makati, 1229 Metro Manila, Philippines",
            "google_maps_link": "https://www.google.com/maps/search/?api=1&query=185+Salcedo+St%2C+Legaspi+Village%2C+Makati%2C+1229+Metro+Manila%2C+Philippines"
        },
        "india": {
            "name": "KBRI New Delhi",
            "aliases": [],
            "link": "https://kemlu.go.id/newdelhi",
            "address": "50-A, Kautilya Marg, Chanakyapuri, New Delhi 110021, India",
            "google_maps_link": "https://www.google.com/maps/search/?api=1&query=50-A%2C+Kautilya+Marg%2C+Chanakyapuri%2C+New+Delhi+110021%2C+India"
        },
        "irak": {
            "name": "KBRI Baghdad",
            "aliases": ["iraq"],
            "link": "https://kemlu.go.id/baghdad",
            "address": "Al-Mansour, Dist. 609, St. 1, Building 21, Baghdad, Iraq",
            "google_maps_link": "https://www.google.com/maps/search/?api=1&query=Al-Mansour%2C+Dist.+609%2C+St.+1%2C+Building+21%2C+Baghdad%2C+Iraq"
        },
        "iran": {
            "name": "KBRI Tehran",
            "aliases": [],
            "link": "https://kemlu.go.id/tehran",
            "address": "No. 34, Zohreh St., Valie Asr Ave., Tehran, Iran",
            "google_maps_link": "https://www.google.com/maps/search/?api=1&query=No.+34%2C+Zohreh+St.%2C+Valie+Asr+Ave.%2C+Tehran%2C+Iran"
        },
        "jepang": {
            "name": "KBRI Tokyo",
            "aliases": ["japan"],
            "link": "https://kemlu.go.id/tokyo",
            "address": "5-9, Higashi Gotanda 5-chome, Shinagawa-ku, Tokyo 141-0022, Japan",
            "google_maps_link": "https://www.google.com/maps/search/?api=1&query=5-9%2C+Higashi+Gotanda+5-chome%2C+Shinagawa-ku%2C+Tokyo+141-0022%2C+Japan"
        },
        "jordania": {
            "name": "KBRI Amman",
            "aliases": ["jordan"],
            "link": "https://kemlu.go.id/amman",
            "address": "Amman, Abdoun Al-Shamali, Abul Harith street No.1, Jordan",
            "google_maps_link": "https://www.google.com/maps/search/?api=1&query=Amman%2C+Abdoun+Al-Shamali%2C+Abul+Harith+street+No.1%2C+Jordan"
        },
        "kamboja": {
            "name": "KBRI Phnom Penh",
            "aliases": ["cambodia"],
            "link": "https://kemlu.go.id/phnompenh",
            "address": "No. 130, Street 466, Sangkat Tonle Bassac, Khan Chamkarmorn, Phnom Penh, Cambodia",
            "google_maps_link": "https://www.google.com/maps/search/?api=1&query=No.+130%2C+Street+466%2C+Sangkat+Tonle+Bassac%2C+Khan+Chamkarmorn%2C+Phnom+Penh%2C+Cambodia"
        },
        "kazakhstan": {
            "name": "KBRI Astana",
            "aliases": [],
            "link": "https://kemlu.go.id/astana",
            "address": "Ul. Kunaeva 29, Astana 010000, Kazakhstan",
            "google_maps_link": "https://www.google.com/maps/search/?api=1&query=Ul.+Kunaeva+29%2C+Astana+010000%2C+Kazakhstan"
        },
        "korea selatan": {
            "name": "KBRI Seoul",
            "aliases": ["south korea", "korsel"],
            "link": "https://kemlu.go.id/seoul",
            "address": "55, Yeouido-dong, Yeongdeungpo-gu, Seoul, Korea Selatan",
            "google_maps_link": "https://www.google.com/maps/search/?api=1&query=55%2C+Yeouido-dong%2C+Yeongdeungpo-gu%2C+Seoul%2C+Korea+Selatan"
        },
        "korea utara": {
            "name": "KBRI Pyongyang",
            "aliases": ["north korea", "korut"],
            "link": "https://kemlu.go.id/pyongyang",
            "address": "Munsudong Diplomatic Compound, Pyongyang, DPR Korea",
            "google_maps_link": "https://www.google.com/maps/search/?api=1&query=Munsudong+Diplomatic+Compound%2C+Pyongyang%2C+DPR+Korea"
        },
        "kuwait": {
            "name": "KBRI Kuwait City",
            "aliases": [],
            "link": "https://kemlu.go.id/kuwaitcity",
            "address": "Area Diplomatic, Block 3, Plot 1, Mishref, Kuwait",
            "google_maps_link": "https://www.google.com/maps/search/?api=1&query=Area+Diplomatic%2C+Block+3%2C+Plot+1%2C+Mishref%2C+Kuwait"
        },
        "laos": {
            "name": "KBRI Vientiane",
            "aliases": [],
            "link": "https://kemlu.go.id/vientiane",
            "address": "Km 4, Thadeua Road, Ban Akat, Vientiane, Laos P.D.R.",
            "google_maps_link": "https://www.google.com/maps/search/?api=1&query=Km+4%2C+Thadeua+Road%2C+Ban+Akat%2C+Vientiane%2C+Laos+P.D.R."
        },
        "lebanon": {
            "name": "KBRI Beirut",
            "aliases": [],
            "link": "https://kemlu.go.id/beirut",
            "address": "Rue 78, General Fouad Chehab, Rabieh, Metn, Lebanon",
            "google_maps_link": "https://www.google.com/maps/search/?api=1&query=Rue+78%2C+General+Fouad+Chehab%2C+Rabieh%2C+Metn%2C+Lebanon"
        },
        "malaysia": {
            "name": "KBRI Kuala Lumpur",
            "aliases": [],
            "link": "https://kemlu.go.id/kualalumpur",
            "address": "233, Jalan Tun Razak, 50400 Kuala Lumpur, Malaysia",
            "google_maps_link": "https://www.google.com/maps/search/?api=1&query=233%2C+Jalan+Tun+Razak%2C+50400+Kuala+Lumpur%2C+Malaysia"
        },
        "myanmar": {
            "name": "KBRI Yangon",
            "aliases": [],
            "link": "https://kemlu.go.id/yangon",
            "address": "100 Pyidaungsu Yeiktha Road, Dagon Township, Yangon, Myanmar",
            "google_maps_link": "https://www.google.com/maps/search/?api=1&query=100+Pyidaungsu+Yeiktha+Road%2C+Dagon+Township%2C+Yangon%2C+Myanmar"
        },
        "oman": {
            "name": "KBRI Muscat",
            "aliases": [],
            "link": "https://kemlu.go.id/muscat",
            "address": "Diplomatic Area, Al Khuwair, P.O. Box 5464, Ruwi, Postal Code 112, Oman",
            "google_maps_link": "https://www.google.com/maps/search/?api=1&query=Diplomatic+Area%2C+Al+Khuwair%2C+Muscat%2C+Oman"
        },
        "pakistan": {
            "name": "KBRI Islamabad",
            "aliases": [],
            "link": "https://kemlu.go.id/islamabad",
            "address": "Diplomatic Enclave II, G-5/4, Islamabad, Pakistan",
            "google_maps_link": "https://www.google.com/maps/search/?api=1&query=Diplomatic+Enclave+II%2C+G-5%2F4%2C+Islamabad%2C+Pakistan"
        },
        "persatuan emirat arab": {
            "name": "KBRI Abu Dhabi",
            "aliases": ["pea", "uae", "uni emirat arab"],
            "link": "https://kemlu.go.id/abudhabi",
            "address": "Plot 49, Sector W59-02, Embassies District, Abu Dhabi, UAE",
            "google_maps_link": "https://www.google.com/maps/search/?api=1&query=Plot+49%2C+Sector+W59-02%2C+Embassies+District%2C+Abu+Dhabi%2C+UAE"
        },
        "ptri asean": {
            "name": "PTRI ASEAN",
            "aliases": [],
            "link": "https://kemlu.go.id/asean",
            "address": "Jl. Sisingamangaraja No.73, Jakarta Selatan, Indonesia",
            "google_maps_link": "https://www.google.com/maps/search/?api=1&query=Jl.+Sisingamangaraja+No.73%2C+Jakarta+Selatan%2C+Indonesia"
        },
        "qatar": {
            "name": "KBRI Doha",
            "aliases": [],
            "link": "https://kemlu.go.id/doha",
            "address": "Diplomatic Area, West Bay, P.O. Box 2769, Doha, Qatar",
            "google_maps_link": "https://www.google.com/maps/search/?api=1&query=Diplomatic+Area%2C+West+Bay%2C+Doha%2C+Qatar"
        },
        "singapura": {
            "name": "KBRI Singapura",
            "aliases": ["singapore"],
            "link": "https://kemlu.go.id/singapore",
            "address": "7 Chatsworth Rd, Singapore 247671",
            "google_maps_link": "https://www.google.com/maps/search/?api=1&query=7+Chatsworth+Rd%2C+Singapore+247671"
        },
        "srilanka": {
            "name": "KBRI Colombo",
            "aliases": ["sri lanka"],
            "link": "https://kemlu.go.id/colombo",
            "address": "153, Dharmapala Mawatha, Colombo 07, Sri Lanka",
            "google_maps_link": "https://www.google.com/maps/search/?api=1&query=153%2C+Dharmapala+Mawatha%2C+Colombo+07%2C+Sri+Lanka"
        },
        "suriah": {
            "name": "KBRI Damascus",
            "aliases": ["syria"],
            "link": "https://kemlu.go.id/damascus",
            "address": "East Mezzeh, Building 45, Damascus, Syria",
            "google_maps_link": "https://www.google.com/maps/search/?api=1&query=East+Mezzeh%2C+Building+45%2C+Damascus%2C+Syria"
        },
        "taiwan": {
            "name": "KDEI Taipei",
            "aliases": [],
            "link": "https://kemlu.go.id/taipei",
            "address": "6F, No.550, Ruiguang Road, Neihu Dist., Taipei City 11492, Taiwan (R.O.C.)",
            "google_maps_link": "https://www.google.com/maps/search/?api=1&query=6F%2C+No.550%2C+Ruiguang+Road%2C+Neihu+Dist.%2C+Taipei+City+11492%2C+Taiwan"
        },
        "thailand": {
            "name": "KBRI Bangkok",
            "aliases": [],
            "link": "https://kemlu.go.id/bangkok",
            "address": "600-604 Phetchaburi Rd, Khwaeng Thanon Phetchaburi, Khet Ratchathewi, Bangkok 10400, Thailand",
            "google_maps_link": "https://www.google.com/maps/search/?api=1&query=600-604+Phetchaburi+Rd%2C+Khwaeng+Thanon+Phetchaburi%2C+Khet+Ratchathewi%2C+Bangkok+10400%2C+Thailand"
        },
        "timor leste": {
            "name": "KBRI Dili",
            "aliases": [],
            "link": "https://kemlu.go.id/dili",
            "address": "Rua Pantai Kelapa, Dili, Timor-Leste",
            "google_maps_link": "https://www.google.com/maps/search/?api=1&query=Rua+Pantai+Kelapa%2C+Dili%2C+Timor-Leste"
        },
        "uzbekistan": {
            "name": "KBRI Tashkent",
            "aliases": [],
            "link": "https://kemlu.go.id/tashkent",
            "address": "Ul. Yahyo G'ulomov 73, Tashkent, Uzbekistan",
            "google_maps_link": "https://www.google.com/maps/search/?api=1&query=Ul.+Yahyo+G'ulomov+73%2C+Tashkent%2C+Uzbekistan"
        },
        "vietnam": {
            "name": "KBRI Hanoi",
            "aliases": [],
            "link": "https://kemlu.go.id/hanoi",
            "address": "50 Ngo Quyen Street, Hoan Kiem District, Hanoi, Vietnam",
            "google_maps_link": "https://www.google.com/maps/search/?api=1&query=50+Ngo+Quyen+Street%2C+Hoan+Kiem+District%2C+Hanoi%2C+Vietnam"
        },
        "yaman": {
            "name": "KBRI Sana'a",
            "aliases": ["yemen"],
            "link": "https://kemlu.go.id/sanaa",
            "address": "Sana'a (Harap cek situs resmi untuk info alamat terkini)",
            "google_maps_link": "https://www.google.com/maps/search/?api=1&query=KBRI+Sana'a"
        },
        "osaka": {
            "name": "KJRI Osaka",
            "aliases": [],
            "link": "https://kemlu.go.id/osaka",
            "address": "Nakanoshima Intes Building 22F, 6-2-40, Nakanoshima, Kita-ku, Osaka 530-0005, Japan",
            "google_maps_link": "https://www.google.com/maps/search/?api=1&query=Nakanoshima+Intes+Building+22F%2C+6-2-40%2C+Nakanoshima%2C+Kita-ku%2C+Osaka+530-0005%2C+Japan"
        }
    },
    "Eropa": {
        "austria": {
            "name": "KBRI Wina",
            "aliases": [],
            "link": "https://kemlu.go.id/vienna",
            "address": "Gustav-Tschermak-Gasse 5-7, 1180 Wien, Austria",
            "google_maps_link": "https://www.google.com/maps/search/?api=1&query=Gustav-Tschermak-Gasse+5-7%2C+1180+Wien%2C+Austria"
        },
        "belanda": {
            "name": "KBRI Den Haag",
            "aliases": ["netherlands", "holland"],
            "link": "https://kemlu.go.id/thehague",
            "address": "Tobias Asserlaan 8, 2517 KC Den Haag, Netherlands",
            "google_maps_link": "https://www.google.com/maps/search/?api=1&query=Tobias+Asserlaan+8%2C+2517+KC+Den+Haag%2C+Netherlands"
        },
        "belgia": {
            "name": "KBRI Brussels",
            "aliases": ["belgium"],
            "link": "https://kemlu.go.id/brussels",
            "address": "Boulevard de la Woluwe 38, 1200 Brussels, Belgium",
            "google_maps_link": "https://www.google.com/maps/search/?api=1&query=Boulevard+de+la+Woluwe+38%2C+1200+Brussels%2C+Belgium"
        },
        "bosnia and herzegovina": {
            "name": "KBRI Sarajevo",
            "aliases": ["bosnia"],
            "link": "https://kemlu.go.id/sarajevo",
            "address": "Splitska 9, Sarajevo 71000, Bosnia and Herzegovina",
            "google_maps_link": "https://www.google.com/maps/search/?api=1&query=Splitska+9%2C+Sarajevo+71000%2C+Bosnia+and+Herzegovina"
        },
        "bulgaria": {
            "name": "KBRI Sofia",
            "aliases": [],
            "link": "https://kemlu.go.id/sofia",
            "address": "Jalan Yosef Valdhard no. 5, 1700 Sofia, Bulgaria",
            "google_maps_link": "https://www.google.com/maps/search/?api=1&query=Jalan+Yosef+Valdhard+no.+5%2C+1700+Sofia%2C+Bulgaria"
        },
        "ceko": {
            "name": "KBRI Praha",
            "aliases": ["czech republic"],
            "link": "https://kemlu.go.id/prague",
            "address": "Nad Budankami II 1944/7, 150 00, Praha 5, Republik Ceko",
            "google_maps_link": "https://www.google.com/maps/search/?api=1&query=Nad+Budankami+II+1944%2F7%2C+150+00%2C+Praha+5%2C+Republik+Ceko"
        },
        "denmark": {
            "name": "KBRI Copenhagen",
            "aliases": [],
            "link": "https://kemlu.go.id/copenhagen",
            "address": "Orehoj Alle 1, 2900 Hellerup, Copenhagen, Denmark",
            "google_maps_link": "https://www.google.com/maps/search/?api=1&query=Orehoj+Alle+1%2C+2900+Hellerup%2C+Copenhagen%2C+Denmark"
        },
        "finlandia": {
            "name": "KBRI Helsinki",
            "aliases": ["finland"],
            "link": "https://kemlu.go.id/helsinki",
            "address": "Kuusisaarentie 3, 00340 Helsinki, Finland",
            "google_maps_link": "https://www.google.com/maps/search/?api=1&query=Kuusisaarentie+3%2C+00340+Helsinki%2C+Finland"
        },
        "hungaria": {
            "name": "KBRI Budapest",
            "aliases": ["hungary"],
            "link": "https://kemlu.go.id/budapest",
            "address": "Gorkij fasor 26, 1071 Budapest, Hungary",
            "google_maps_link": "https://www.google.com/maps/search/?api=1&query=Gorkij+fasor+26%2C+1071+Budapest%2C+Hungary"
        },
        "inggris": {
            "name": "KBRI London",
            "aliases": ["uk", "united kingdom", "britania raya"],
            "link": "https://kemlu.go.id/london",
            "address": "38 Grosvenor Square, London W1K 2HW, United Kingdom",
            "google_maps_link": "https://www.google.com/maps/search/?api=1&query=38+Grosvenor+Square%2C+London+W1K+2HW%2C+United+Kingdom"
        },
        "italia": {
            "name": "KBRI Roma",
            "aliases": ["italy"],
            "link": "https://kemlu.go.id/rome",
            "address": "Via Campania, 55, 00187 Roma RM, Italy",
            "google_maps_link": "https://www.google.com/maps/search/?api=1&query=Via+Campania%2C+55%2C+00187+Roma+RM%2C+Italy"
        },
        "jerman": {
            "name": "KBRI Berlin",
            "aliases": ["germany"],
            "link": "https://kemlu.go.id/berlin",
            "address": "Lehrter Str. 16-17, 10557 Berlin, Germany",
            "google_maps_link": "https://www.google.com/maps/search/?api=1&query=Lehrter+Str.+16-17%2C+10557+Berlin%2C+Germany"
        },
        "kroasia": {
            "name": "KBRI Zagreb",
            "aliases": ["croatia"],
            "link": "https://kemlu.go.id/zagreb",
            "address": "Medvedgradska 13, 10000 Zagreb, Croatia",
            "google_maps_link": "https://www.google.com/maps/search/?api=1&query=Medvedgradska+13%2C+10000+Zagreb%2C+Croatia"
        },
        "norwegia": {
            "name": "KBRI Oslo",
            "aliases": ["norway"],
            "link": "https://kemlu.go.id/oslo",
            "address": "Fritzners gate 12, 0264 Oslo, Norway",
            "google_maps_link": "https://www.google.com/maps/search/?api=1&query=Fritzners+gate+12%2C+0264+Oslo%2C+Norway"
        },
        "polandia": {
            "name": "KBRI Warsawa",
            "aliases": ["poland"],
            "link": "https://kemlu.go.id/warsaw",
            "address": "Ul. Estońska 3/5, 03-903 Warszawa, Poland",
            "google_maps_link": "https://www.google.com/maps/search/?api=1&query=Ul.+Esto%C5%84ska+3%2F5%2C+03-903+Warszawa%2C+Poland"
        },
        "portugal": {
            "name": "KBRI Lisbon",
            "aliases": [],
            "link": "https://kemlu.go.id/lisbon",
            "address": "Rua D. Lourenço de Almeida, 2-A, 1400-111 Lisboa, Portugal",
            "google_maps_link": "https://www.google.com/maps/search/?api=1&query=Rua+D.+Louren%C3%A7o+de+Almeida%2C+2-A%2C+1400-111+Lisboa%2C+Portugal"
        },
        "prancis": {
            "name": "KBRI Paris",
            "aliases": ["france"],
            "link": "https://kemlu.go.id/paris",
            "address": "47-49 Rue Cortambert, 75116 Paris, France",
            "google_maps_link": "https://www.google.com/maps/search/?api=1&query=47-49+Rue+Cortambert%2C+75116+Paris%2C+France"
        },
        "ptri jenewa": {
            "name": "PTRI Jenewa",
            "aliases": [],
            "link": "https://kemlu.go.id/geneva",
            "address": "Rue de Saint-Jean 16, 1203 Genève, Switzerland",
            "google_maps_link": "https://www.google.com/maps/search/?api=1&query=Rue+de+Saint-Jean+16%2C+1203+Gen%C3%A8ve%2C+Switzerland"
        },
        "rumania": {
            "name": "KBRI Bucharest",
            "aliases": ["romania"],
            "link": "https://kemlu.go.id/bucharest",
            "address": "Strada Gina Patrichi 10, București 010831, Romania",
            "google_maps_link": "https://www.google.com/maps/search/?api=1&query=Strada+Gina+Patrichi+10%2C+Bucure%C8%99ti+010831%2C+Romania"
        },
        "rusia": {
            "name": "KBRI Moscow",
            "aliases": ["russia"],
            "link": "https://kemlu.go.id/moscow",
            "address": "Novokuznetskaya Ulitsa, 12, Moscow, Russia, 115184",
            "google_maps_link": "https://www.google.com/maps/search/?api=1&query=Novokuznetskaya+Ulitsa%2C+12%2C+Moscow%2C+Russia%2C+115184"
        },
        "serbia": {
            "name": "KBRI Belgrade",
            "aliases": [],
            "link": "https://kemlu.go.id/belgrade",
            "address": "Bulevar Kneza Aleksandra Karadjordjevica 40, Belgrade, Serbia",
            "google_maps_link": "https://www.google.com/maps/search/?api=1&query=Bulevar+Kneza+Aleksandra+Karadjordjevica+40%2C+Belgrade%2C+Serbia"
        },
        "slovakia": {
            "name": "KBRI Bratislava",
            "aliases": [],
            "link": "https://kemlu.go.id/bratislava",
            "address": "Drotárska cesta 134, 841 04 Bratislava, Slovakia",
            "google_maps_link": "https://www.google.com/maps/search/?api=1&query=Drot%C3%A1rska+cesta+134%2C+841+04+Bratislava%2C+Slovakia"
        },
        "spanyol": {
            "name": "KBRI Madrid",
            "aliases": ["spain"],
            "link": "https://kemlu.go.id/madrid",
            "address": "Calle Emilio Vargas, 3, 28043 Madrid, Spain",
            "google_maps_link": "https://www.google.com/maps/search/?api=1&query=Calle+Emilio+Vargas%2C+3%2C+28043+Madrid%2C+Spain"
        },
        "swedia": {
            "name": "KBRI Stockholm",
            "aliases": ["sweden"],
            "link": "https://kemlu.go.id/stockholm",
            "address": "Kungsbroplan 1, 112 27 Stockholm, Sweden",
            "google_maps_link": "https://www.google.com/maps/search/?api=1&query=Kungsbroplan+1%2C+112+27+Stockholm%2C+Sweden"
        },
        "swiss": {
            "name": "KBRI Bern",
            "aliases": ["switzerland"],
            "link": "https://kemlu.go.id/bern",
            "address": "Elfenauweg 51, 3006 Bern, Switzerland",
            "google_maps_link": "https://www.google.com/maps/search/?api=1&query=Elfenauweg+51%2C+3006+Bern%2C+Switzerland"
        },
        "turkiye": {
            "name": "KBRI Ankara",
            "aliases": ["turkey"],
            "link": "https://kemlu.go.id/ankara",
            "address": "Refik Belendir Sokak No:1, Gaziosmanpaşa, Çankaya/Ankara, Turkey",
            "google_maps_link": "https://www.google.com/maps/search/?api=1&query=Refik+Belendir+Sokak+No%3A1%2C+Gaziosmanpa%C5%9Fa%2C+%C3%87ankaya%2FAnkara%2C+Turkey"
        },
        "ukraina": {
            "name": "KBRI Kyiv",
            "aliases": ["ukraine"],
            "link": "https://kemlu.go.id/kyiv",
            "address": "Ul. Otto Shmidta 1, Kyiv, Ukraine, 04107",
            "google_maps_link": "https://www.google.com/maps/search/?api=1&query=Ul.+Otto+Shmidta+1%2C+Kyiv%2C+Ukraine%2C+04107"
        },
        "vatikan": {
            "name": "KBRI Takhta Suci Vatikan",
            "aliases": ["vatican"],
            "link": "https://kemlu.go.id/vatikan",
            "address": "Via Aurelia 226, 00165 Roma RM, Italy",
            "google_maps_link": "https://www.google.com/maps/search/?api=1&query=Via+Aurelia+226%2C+00165+Roma+RM%2C+Italy"
        },
        "yunani": {
            "name": "KBRI Athena",
            "aliases": ["greece"],
            "link": "https://kemlu.go.id/athens",
            "address": "Mesogeion Ave 201, Cholargos 155 61, Greece",
            "google_maps_link": "https://www.google.com/maps/search/?api=1&query=Mesogeion+Ave+201%2C+Cholargos+155+61%2C+Greece"
        }
    },
    "Afrika": {
        "afrika selatan": {
            "name": "KBRI Pretoria",
            "aliases": ["south africa"],
            "link": "https://kemlu.go.id/pretoria",
            "address": "949 Francis Baard St. Arcadia, Pretoria 0007, Afrika Selatan",
            "google_maps_link": "https://www.google.com/maps/search/?api=1&query=949+Francis+Baard+St.+Arcadia%2C+Pretoria+0007%2C+Afrika+Selatan"
        },
        "aljazair": {
            "name": "KBRI Algiers",
            "aliases": ["algeria"],
            "link": "https://kemlu.go.id/algiers",
            "address": "Villa No. 17, Domaine Chekiken, Ben Aknoun, Alger, Aljazair",
            "google_maps_link": "https://www.google.com/maps/search/?api=1&query=Villa+No.+17%2C+Domaine+Chekiken%2C+Ben+Aknoun%2C+Alger%2C+Aljazair"
        },
        "ethiopia": {
            "name": "KBRI Addis Ababa",
            "aliases": [],
            "link": "https://kemlu.go.id/addisababa",
            "address": "Gurd Shola, Comoros St., P.O. Box 1004, Addis Ababa, Ethiopia",
            "google_maps_link": "https://www.google.com/maps/search/?api=1&query=Gurd+Shola%2C+Comoros+St.%2C+Addis+Ababa%2C+Ethiopia"
        },
        "kamerun": {
            "name": "KBRI Yaounde",
            "aliases": ["cameroon"],
            "link": "https://kemlu.go.id/yaounde",
            "address": "Rue 1.701, Bastos, B.P. 7454, Yaounde, Cameroon",
            "google_maps_link": "https://www.google.com/maps/search/?api=1&query=Rue+1.701%2C+Bastos%2C+Yaounde%2C+Cameroon"
        },
        "kenya": {
            "name": "KBRI Nairobi",
            "aliases": [],
            "link": "https://kemlu.go.id/nairobi",
            "address": "Arboretum Road, Nairobi, Kenya",
            "google_maps_link": "https://www.google.com/maps/search/?api=1&query=Arboretum+Road%2C+Nairobi%2C+Kenya"
        },
        "libya": {
            "name": "KBRI Tripoli",
            "aliases": [],
            "link": "https://kemlu.go.id/tripoli",
            "address": "Area 3, Diplomatic Quarters, P.O. Box 1025, Tripoli, Libya",
            "google_maps_link": "https://www.google.com/maps/search/?api=1&query=Area+3%2C+Diplomatic+Quarters%2C+Tripoli%2C+Libya"
        },
        "madagaskar": {
            "name": "KBRI Antananarivo",
            "aliases": ["madagascar"],
            "link": "https://kemlu.go.id/antananarivo",
            "address": "Lot II L 10 Bis, Ter Rue Ratsimamanaga, Ambodirotra, Antananarivo 101, Madagascar",
            "google_maps_link": "https://www.google.com/maps/search/?api=1&query=Lot+II+L+10+Bis%2C+Ter+Rue+Ratsimamanaga%2C+Ambodirotra%2C+Antananarivo+101%2C+Madagascar"
        },
        "maroko": {
            "name": "KBRI Rabat",
            "aliases": ["morocco"],
            "link": "https://kemlu.go.id/rabat",
            "address": "67, Rue Patrice Lumumba, Agdal, Rabat, Morocco",
            "google_maps_link": "https://www.google.com/maps/search/?api=1&query=67%2C+Rue+Patrice+Lumumba%2C+Agdal%2C+Rabat%2C+Morocco"
        },
        "mesir": {
            "name": "KBRI Kairo",
            "aliases": ["egypt"],
            "link": "https://kemlu.go.id/cairo",
            "address": "13, Aisha Al-Taymouriya St., Garden City, Cairo, Egypt",
            "google_maps_link": "https://www.google.com/maps/search/?api=1&query=13%2C+Aisha+Al-Taymouriya+St.%2C+Garden+City%2C+Cairo%2C+Egypt"
        },
        "mozambique": {
            "name": "KBRI Maputo",
            "aliases": ["mozambik"],
            "link": "https://kemlu.go.id/maputo",
            "address": "Av. Julius Nyerere No. 1290, Maputo, Mozambique",
            "google_maps_link": "https://www.google.com/maps/search/?api=1&query=Av.+Julius+Nyerere+No.+1290%2C+Maputo%2C+Mozambique"
        },
        "namibia": {
            "name": "KBRI Windhoek",
            "aliases": [],
            "link": "https://kemlu.go.id/windhoek",
            "address": "5778 Republic Road, Eros, Windhoek, Namibia",
            "google_maps_link": "https://www.google.com/maps/search/?api=1&query=5778+Republic+Road%2C+Eros%2C+Windhoek%2C+Namibia"
        },
        "nigeria": {
            "name": "KBRI Abuja",
            "aliases": [],
            "link": "https://kemlu.go.id/abuja",
            "address": "10, Udo Udoma Street, Central Business District, Abuja, Nigeria",
            "google_maps_link": "https://www.google.com/maps/search/?api=1&query=10%2C+Udo+Udoma+Street%2C+Central+Business+District%2C+Abuja%2C+Nigeria"
        },
        "senegal": {
            "name": "KBRI Dakar",
            "aliases": [],
            "link": "https://kemlu.go.id/dakar",
            "address": "Rue 1 x Boulevard du Sud, Fann Résidence, BP 1709 Dakar, Senegal",
            "google_maps_link": "https://www.google.com/maps/search/?api=1&query=Rue+1+x+Boulevard+du+Sud%2C+Fann+R%C3%A9sidence%2C+Dakar%2C+Senegal"
        },
        "sudan": {
            "name": "KBRI Khartoum",
            "aliases": [],
            "link": "https://kemlu.go.id/khartoum",
            "address": "Al-Amart, Street 19, House No. 1, Khartoum, Sudan",
            "google_maps_link": "https://www.google.com/maps/search/?api=1&query=Al-Amart%2C+Street+19%2C+House+No.+1%2C+Khartoum%2C+Sudan"
        },
        "tanzania": {
            "name": "KBRI Dar es Salaam",
            "aliases": [],
            "link": "https://kemlu.go.id/daressalaam",
            "address": "Bima Street No. 367, Upanga, P.O. Box 572, Dar es Salaam, Tanzania",
            "google_maps_link": "https://www.google.com/maps/search/?api=1&query=Bima+Street+No.+367%2C+Upanga%2C+Dar+es+Salaam%2C+Tanzania"
        },
        "tunisia": {
            "name": "KBRI Tunis",
            "aliases": [],
            "link": "https://kemlu.go.id/tunis",
            "address": "Rue du Lac Lochness, Les Berges du Lac, Tunis 1053, Tunisia",
            "google_maps_link": "https://www.google.com/maps/search/?api=1&query=Rue+du+Lac+Lochness%2C+Les+Berges+du+Lac%2C+Tunis+1053%2C+Tunisia"
        },
        "zimbabwe": {
            "name": "KBRI Harare",
            "aliases": [],
            "link": "https://kemlu.go.id/harare",
            "address": "10 Natal Road, Belgravia, Harare, Zimbabwe",
            "google_maps_link": "https://www.google.com/maps/search/?api=1&query=10+Natal+Road%2C+Belgravia%2C+Harare%2C+Zimbabwe"
        }
    },
    "Amerika": {
        "amerika serikat": {
            "name": "KBRI Washington D.C.",
            "aliases": ["usa", "united states", "as"],
            "link": "https://kemlu.go.id/washington",
            "address": "2020 Massachusetts Ave NW, Washington, DC 20036, USA",
            "google_maps_link": "https://www.google.com/maps/search/?api=1&query=2020+Massachusetts+Ave+NW%2C+Washington%2C+DC+20036%2C+USA"
        },
        "argentina": {
            "name": "KBRI Buenos Aires",
            "aliases": [],
            "link": "https://kemlu.go.id/buenosaires",
            "address": "Mariscal Ramon Castilla 2901, 1425 Buenos Aires, Argentina",
            "google_maps_link": "https://www.google.com/maps/search/?api=1&query=Mariscal+Ramon+Castilla+2901%2C+1425+Buenos+Aires%2C+Argentina"
        },
        "brazil": {
            "name": "KBRI Brasilia",
            "aliases": ["brasil"],
            "link": "https://kemlu.go.id/brasilia",
            "address": "SES Avenida Das Nacoes Quadra 805, Lote. 20, Brasilia-DF, Brazil",
            "google_maps_link": "https://www.google.com/maps/search/?api=1&query=SES+Avenida+Das+Nacoes+Quadra+805%2C+Lote.+20%2C+Brasilia-DF%2C+Brazil"
        },
        "chile": {
            "name": "KBRI Santiago",
            "aliases": ["chili"],
            "link": "https://kemlu.go.id/santiago",
            "address": "Av. Las Urbinas 160, Providencia, Santiago, Chile",
            "google_maps_link": "https://www.google.com/maps/search/?api=1&query=Av.+Las+Urbinas+160%2C+Providencia%2C+Santiago%2C+Chile"
        },
        "ecuador": {
            "name": "KBRI Quito",
            "aliases": ["ekuador"],
            "link": "https://kemlu.go.id/quito",
            "address": "Av. República de El Salvador N34-111 y Av. Portugal, Quito, Ecuador",
            "google_maps_link": "https://www.google.com/maps/search/?api=1&query=Av.+Rep%C3%BAblica+de+El+Salvador+N34-111+y+Av.+Portugal%2C+Quito%2C+Ecuador"
        },
        "kanada": {
            "name": "KBRI Ottawa",
            "aliases": ["canada"],
            "link": "https://kemlu.go.id/ottawa",
            "address": "55 Parkdale Ave, Ottawa, ON K1Y 1E5, Canada",
            "google_maps_link": "https://www.google.com/maps/search/?api=1&query=55+Parkdale+Ave%2C+Ottawa%2C+ON+K1Y+1E5%2C+Canada"
        },
        "kolombia": {
            "name": "KBRI Bogota",
            "aliases": ["colombia"],
            "link": "https://kemlu.go.id/bogota",
            "address": "Carrera 11 No. 75-01, Bogota D.C., Colombia",
            "google_maps_link": "https://www.google.com/maps/search/?api=1&query=Carrera+11+No.+75-01%2C+Bogota+D.C.%2C+Colombia"
        },
        "kuba": {
            "name": "KBRI Havana",
            "aliases": ["cuba"],
            "link": "https://kemlu.go.id/havana",
            "address": "Calle 76 No. 5101, entre 5ta y 5ta A, Reparto Miramar, Havana, Cuba",
            "google_maps_link": "https://www.google.com/maps/search/?api=1&query=Calle+76+No.+5101%2C+entre+5ta+y+5ta+A%2C+Reparto+Miramar%2C+Havana%2C+Cuba"
        },
        "meksiko": {
            "name": "KBRI Mexico City",
            "aliases": ["mexico"],
            "link": "https://kemlu.go.id/mexicocity",
            "address": "Julio Verne 13, Col. Polanco, C.P. 11560, Mexico City, Mexico",
            "google_maps_link": "https://www.google.com/maps/search/?api=1&query=Julio+Verne+13%2C+Col.+Polanco%2C+C.P.+11560%2C+Mexico+City%2C+Mexico"
        },
        "panama": {
            "name": "KBRI Panama City",
            "aliases": [],
            "link": "https://kemlu.go.id/panamacity",
            "address": "Calle 50, Edificio Global Plaza, Oficina 20-A, Panama City, Panama",
            "google_maps_link": "https://www.google.com/maps/search/?api=1&query=Calle+50%2C+Edificio+Global+Plaza%2C+Oficina+20-A%2C+Panama+City%2C+Panama"
        },
        "peru": {
            "name": "KBRI Lima",
            "aliases": [],
            "link": "https://kemlu.go.id/lima",
            "address": "Av. Las Flores 375, San Isidro, Lima 27, Peru",
            "google_maps_link": "https://www.google.com/maps/search/?api=1&query=Av.+Las+Flores+375%2C+San+Isidro%2C+Lima+27%2C+Peru"
        },
        "suriname": {
            "name": "KBRI Paramaribo",
            "aliases": [],
            "link": "https://kemlu.go.id/paramaribo",
            "address": "Anton Drachtenweg 241, Paramaribo, Suriname",
            "google_maps_link": "https://www.google.com/maps/search/?api=1&query=Anton+Drachtenweg+241%2C+Paramaribo%2C+Suriname"
        },
        "venezuela": {
            "name": "KBRI Caracas",
            "aliases": [],
            "link": "https://kemlu.go.id/caracas",
            "address": "Av. Francisco de Miranda, Edificio Centro Seguros La Paz, Piso 10, Caracas, Venezuela",
            "google_maps_link": "https://www.google.com/maps/search/?api=1&query=Av.+Francisco+de+Miranda%2C+Edificio+Centro+Seguros+La+Paz%2C+Piso+10%2C+Caracas%2C+Venezuela"
        },
        "los angeles": {
            "name": "KJRI Los Angeles",
            "aliases": [],
            "link": "https://kemlu.go.id/losangeles",
            "address": "3457 Wilshire Blvd, Los Angeles, CA 90010, USA",
            "google_maps_link": "https://www.google.com/maps/search/?api=1&query=3457+Wilshire+Blvd%2C+Los+Angeles%2C+CA+90010%2C+USA"
        },
        "new york": {
            "name": "KJRI New York",
            "aliases": [],
            "link": "https://kemlu.go.id/newyork",
            "address": "5 East 68th Street, New York, NY 10065, USA",
            "google_maps_link": "https://www.google.com/maps/search/?api=1&query=5+East+68th+Street%2C+New+York%2C+NY+10065%2C+USA"
        },
        "san francisco": {
            "name": "KJRI San Francisco",
            "aliases": [],
            "link": "https://kemlu.go.id/sanfrancisco",
            "address": "1111 Columbus Avenue, San Francisco, CA 94133, USA",
            "google_maps_link": "https://www.google.com/maps/search/?api=1&query=1111+Columbus+Avenue%2C+San+Francisco%2C+CA+94133%2C+USA"
        },
        "houston": {
            "name": "KJRI Houston",
            "aliases": [],
            "link": "https://kemlu.go.id/houston",
            "address": "10900 Richmond Ave, Houston, TX 77042, USA",
            "google_maps_link": "https://www.google.com/maps/search/?api=1&query=10900+Richmond+Ave%2C+Houston%2C+TX+77042%2C+USA"
        }
    },
    "Australia & Oseania": {
        "australia": {
            "name": "KBRI Canberra",
            "aliases": ["aussie"],
            "link": "https://kemlu.go.id/canberra",
            "address": "8 Darwin Ave, Yarralumla ACT 2600, Australia",
            "google_maps_link": "https://www.google.com/maps/search/?api=1&query=8+Darwin+Ave%2C+Yarralumla+ACT+2600%2C+Australia"
        },
        "fiji": {
            "name": "KBRI Suva",
            "aliases": [],
            "link": "https://kemlu.go.id/suva",
            "address": "6th Floor, FNPF Place, 343-359 Victoria Parade, Suva, Fiji",
            "google_maps_link": "https://www.google.com/maps/search/?api=1&query=6th+Floor%2C+FNPF+Place%2C+343-359+Victoria+Parade%2C+Suva%2C+Fiji"
        },
        "new caledonia": {
            "name": "KJRI Noumea",
            "aliases": ["kaledonia baru"],
            "link": "https://kemlu.go.id/noumea",
            "address": "15, Rue de la Somme, Magenta, Noumea, New Caledonia",
            "google_maps_link": "https://www.google.com/maps/search/?api=1&query=15%2C+Rue+de+la+Somme%2C+Magenta%2C+Noumea%2C+New+Caledonia"
        },
        "papua nugini": {
            "name": "KBRI Port Moresby",
            "aliases": ["papua new guinea"],
            "link": "https://kemlu.go.id/portmoresby",
            "address": "P.O. Box 7183, Boroko, NCD, Port Moresby, Papua New Guinea",
            "google_maps_link": "https://www.google.com/maps/search/?api=1&query=Indonesian+Embassy%2C+Port+Moresby%2C+Papua+New+Guinea"
        },
        "selandia baru": {
            "name": "KBRI Wellington",
            "aliases": ["new zealand", "nz"],
            "link": "https://kemlu.go.id/wellington",
            "address": "70 Glenmore Street, Thorndon, Wellington 6012, New Zealand",
            "google_maps_link": "https://www.google.com/maps/search/?api=1&query=70+Glenmore+Street%2C+Thorndon%2C+Wellington+6012%2C+New+Zealand"
        },
        "sydney": {
            "name": "KJRI Sydney",
            "aliases": [],
            "link": "https://kemlu.go.id/sydney",
            "address": "236-238 Maroubra Rd, Maroubra NSW 2035, Australia",
            "google_maps_link": "https://www.google.com/maps/search/?api=1&query=236-238+Maroubra+Rd%2C+Maroubra+NSW+2035%2C+Australia"
        },
        "melbourne": {
            "name": "KJRI Melbourne",
            "aliases": [],
            "link": "https://kemlu.go.id/melbourne",
            "address": "72 Queens Rd, Melbourne VIC 3004, Australia",
            "google_maps_link": "https://www.google.com/maps/search/?api=1&query=72+Queens+Rd%2C+Melbourne+VIC+3004%2C+Australia"
        },
        "perth": {
            "name": "KJRI Perth",
            "aliases": [],
            "link": "https://kemlu.go.id/perth",
            "address": "134 Adelaide Terrace, East Perth WA 6004, Australia",
            "google_maps_link": "https://www.google.com/maps/search/?api=1&query=134+Adelaide+Terrace%2C+East+Perth+WA+6004%2C+Australia"
        }
    }
}