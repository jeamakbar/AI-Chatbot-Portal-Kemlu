# --- APPLICATION CONSTANTS ---
LLM_API_URL = "https://openrouter.ai/api/v1/chat/completions"
RESPONSE_SEPARATOR = "###"
MAX_CONVERSATION_HISTORY = 10

# --- REGEX PATTERNS ---
ADDRESS_KEYWORDS_PATTERN = r"(alamat|lokasi|di mana|address|location|where is|dimana).*?(kbri|konsulat|kedutaan|perwakilan|kdei|embassy|consulate|representation)\s*(?:di|di negara|untuk)?\s*([\w\s\.]*?)[\?\.!\s]*$"
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
        r"kekonsuleran|konsuler": (
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
        r"consular": (
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

LLM_SYSTEM_PROMPTS = {
    "en": (
        "## Persona\n"
        "You are 'Sahabat Kemlu', the highly professional, empathetic, and accurate AI Virtual Assistant for the Ministry of Foreign Affairs of the Republic of Indonesia. Your primary role is to provide clear, reliable, and concise information regarding all services offered by the Ministry and its representative offices (Embassies/KBRI and Consulate Generals/KJRI) worldwide. Your communication style is formal yet friendly.\n\n"
        "## Core Directives\n"
        "1.  **Absolute Source of Truth:** All your answers **must** be derived **exclusively** from the content available on `kemlu.go.id` and the internal data provided. Do not invent information or use external knowledge.\n"
        "2.  **Strict Scope of Service:** If a query is outside the scope of the Ministry of Foreign Affairs of Indonesia (e.g., domestic policies, other ministries), you **must** reply with: \"I can only provide information regarding the services of the Ministry of Foreign Affairs of the Republic of Indonesia and its representatives abroad. For other matters, please consult the relevant authorities.\"\n"
        "3.  **Handling Missing Information:** If a query is within scope but the information is not on `kemlu.go.id` or in internal data, you **must** reply with: \"Information regarding your query is not available on the kemlu.go.id website. For the most accurate details, please visit the official website directly or contact the nearest Indonesian Representative Office.\"\n\n"
        "## Response Format\n"
        "Use simple HTML for structure (<strong> for titles, <ul>/<ol> for lists, <p> for paragraphs, and <a> for links). You are **strictly forbidden** from creating `<a>` HTML tags directly. If you need to refer to a webpage, use a special placeholder format: `[LINK:context]`. The system will automatically convert this into a correct link. Example: `For more information, please visit [LINK:Consular Services]`."
    ),
    "id": (
        "## Persona\n"
        "Anda adalah 'Sahabat Kemlu', Asisten Virtual AI dari Kementerian Luar Negeri RI yang sangat profesional, empatik, dan akurat. Peran utama Anda adalah memberikan informasi yang jelas, terpercaya, dan ringkas mengenai keseluruhan layanan Kementerian Luar Negeri dan semua perwakilannya (KBRI dan KJRI) di seluruh dunia. Gaya komunikasi Anda formal namun tetap ramah.\n\n"
        "## Arahan Utama\n"
        "1.  **Sumber Tunggal Absolut:** Semua jawaban Anda **wajib** bersumber **eksklusif** dari konten yang tersedia di `kemlu.go.id` dan data internal yang diberikan. Jangan mengarang informasi atau menggunakan pengetahuan eksternal.\n"
        "2.  **Lingkup Layanan yang Ketat:** Jika pertanyaan di luar lingkup Kementerian Luar Negeri RI (misal: kebijakan dalam negeri, kementerian lain), Anda **wajib** membalas dengan: \"Saya hanya dapat memberikan informasi seputar layanan Kementerian Luar Negeri RI dan perwakilannya di luar negeri. Untuk urusan lain, silakan hubungi pihak yang berwenang.\"\n"
        "3.  **Penanganan Informasi Nihil:** Jika informasi yang dicari dalam lingkup Kemlu namun tidak ada di `kemlu.go.id` atau data internal, Anda **wajib** membalas dengan: \"Informasi mengenai permintaan Anda tidak tersedia di situs kemlu.go.id. Untuk detail yang paling akurat, silakan kunjungi situs web resmi secara langsung atau hubungi Perwakilan RI terdekat.\"\n\n"
        "## Format Jawaban\n"
        "Gunakan HTML sederhana untuk struktur (<strong> untuk judul, <ul>/<ol> untuk daftar, <p> untuk paragraf, dan <a> untuk tautan). Anda **dilarang keras** membuat tag HTML `<a>` secara langsung. Jika Anda perlu merujuk ke halaman situs web, gunakan format placeholder khusus: `[LINK:konteks]`. Sistem akan secara otomatis mengubahnya menjadi tautan yang benar. Contoh: `Untuk informasi lebih lanjut, silakan kunjungi [LINK:Layanan Konsuler]`."
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
    {
        "pattern": r"lapor diri",
        "priority": 10,
        "context": "lapor diri",
        "answer": (
            "<strong>Prosedur Lapor Diri Online untuk WNI di Luar Negeri</strong>"
            "<p>Warga Negara Indonesia (WNI) yang berada di luar negeri sangat dianjurkan untuk melakukan Lapor Diri secara daring melalui Portal Peduli WNI. Berikut langkah-langkahnya:</p>"
            "<strong>Langkah-langkah Lapor Diri Online:</strong>"
            "<ul>"
            "<li>Kunjungi situs resmi di: <a href='https://peduliwni.kemlu.go.id' target='_blank'>https://peduliwni.kemlu.go.id</a>.</li>"
            "<li><strong>Buat Akun atau Masuk:</strong> Jika belum memiliki akun, silakan mendaftar terlebih dahulu.</li>"
            "<li><strong>Isi Formulir:</strong> Isi formulir Lapor Diri secara lengkap dengan data pribadi, informasi paspor, alamat tinggal di luar negeri, dan kontak darurat.</li>"
            "<li><strong>Unggah Dokumen:</strong> Siapkan dan unggah dokumen pendukung seperti salinan paspor dan bukti izin tinggal (contoh: visa atau KTP setempat).</li>"
            "<li><strong>Simpan Bukti:</strong> Setelah selesai, pastikan Anda menyimpan bukti registrasi Lapor Diri Anda.</li>"
            "</ul>"
            "<strong>Manfaat Lapor Diri:</strong>"
            "<ul>"
            "<li>Memudahkan Perwakilan RI (KBRI/KJRI) dalam memberikan layanan dan perlindungan.</li>"
            "<li>Menjadi salah satu persyaratan untuk pengajuan layanan kekonsuleran.</li>"
            "</ul>"
        ),
        "follow_up": ["Dokumen apa saja yang perlu diunggah?", "Apakah lapor diri itu wajib?", "Berapa lama proses verifikasi lapor diri?"]
    },
    {
        "pattern": r"(prosedur|syarat|cara|membuat|perpanjang|biometrik|dokumen).*(paspor)",
        "priority": 10,
        "context": "layanan konsuler",
        "answer": (
            "<strong>Pengajuan atau Perpanjangan Paspor Indonesia</strong>"
            "<p>Berikut adalah langkah-langkah dan persyaratan umum untuk mengajukan atau memperpanjang paspor Indonesia:</p>"
            "<strong>Langkah-langkah Umum:</strong>"
            "<ul>"
            "<li><strong>Buat Janji Temu Online:</strong> Umumnya, Anda perlu membuat janji temu melalui situs web atau aplikasi resmi Kantor Imigrasi (jika di Indonesia) atau Perwakilan RI (jika di luar negeri).</li>"
            "<li><strong>Datang ke Lokasi:</strong> Hadir sesuai jadwal untuk verifikasi data, pengambilan foto, dan sidik jari (biometrik).</li>"
            "<li><strong>Wawancara Singkat:</strong> Petugas akan melakukan wawancara singkat untuk verifikasi.</li>"
            "<li><strong>Lakukan Pembayaran:</strong> Bayar biaya paspor sesuai ketentuan yang berlaku.</li>"
            "</ul>"
            "<strong>Dokumen yang Diperlukan (Asli dan Fotokopi):</strong>"
            "<ul>"
            "<li><strong>E-KTP</strong> yang masih berlaku.</li>"
            "<li><strong>Kartu Keluarga (KK)</strong>.</li>"
            "<li><strong>Salah satu dari dokumen berikut:</strong> Akta Kelahiran, Ijazah (SD/SMP/SMA), atau Buku Nikah.</li>"
            "<li><strong>Paspor Lama:</strong> Wajib dibawa jika Anda ingin memperpanjang paspor.</li>"
            "</ul>"
            "<p><em><strong>Catatan Penting:</strong> Persyaratan di luar negeri mungkin sedikit berbeda. Selalu periksa situs web Perwakilan RI terdekat untuk informasi paling akurat.</em></p>"
        ),
        "follow_up": ["Berapa biaya pembuatan paspor?", "Berapa lama prosesnya sampai paspor jadi?", "Apa bedanya paspor biasa dan e-paspor?"]
    },
    {
        "pattern": r"(syarat|prosedur|cara|biaya).*(legalisasi|legalisir).*(dokumen)",
        "priority": 9,
        "context": "legalisasi dokumen",
        "answer": (
            '<strong>Layanan Legalisasi Dokumen</strong>'
            '<p>Legalisasi adalah proses pengesahan tanda tangan pejabat dan/atau stempel resmi pada suatu dokumen. Berikut adalah informasi umum berdasarkan skenario yang paling umum:</p>'
            '<strong>1. Legalisasi Dokumen di Perwakilan RI (KBRI/KJRI)</strong>'
            '<p>Ini berlaku untuk dokumen yang diterbitkan di luar negeri untuk digunakan di Indonesia, atau sebaliknya. Persyaratan umum meliputi:</p>'
            '<ul>'
            '<li><strong>Dokumen Asli:</strong> Dokumen yang akan dilegalisasi.</li>'
            '<li><strong>Terjemahan (jika perlu):</strong> Dokumen berbahasa asing harus diterjemahkan ke Bahasa Indonesia oleh penerjemah tersumpah.</li>'
            '<li><strong>Identitas Diri:</strong> Fotokopi paspor atau KTP pemohon.</li>'
            '<li><strong>Formulir Permohonan:</strong> Mengisi formulir yang disediakan oleh Perwakilan RI.</li>'
            '<li><strong>Biaya:</strong> Membayar biaya sesuai tarif yang berlaku.</li>'
            '</ul>'
            '<strong>2. Legalisasi Dokumen di Indonesia (untuk Penggunaan di Luar Negeri)</strong>'
            '<p>Untuk dokumen yang diterbitkan di Indonesia dan akan digunakan di negara lain, alurnya adalah sebagai berikut:</p>'
            '<ol>'
            '<li><strong>Kementerian Hukum dan HAM (Kemenkumham):</strong> Dokumen harus dilegalisasi terlebih dahulu di Direktorat Perdata, Ditjen AHU Kemenkumham.</li>'
            '<li><strong>Kementerian Luar Negeri (Kemenlu):</strong> Setelah dari Kemenkumham, dokumen dilegalisasi di Direktorat Konsuler Kemenlu.</li>'
            '<li><strong>Kedutaan Negara Tujuan:</strong> Tahap akhir adalah legalisasi di Kedutaan Besar atau Konsulat negara yang dituju di Jakarta.</li>'
            '</ol>'
            '<p><em><strong>Catatan Penting:</strong> Untuk negara-negara anggota Konvensi Apostille, prosesnya lebih sederhana dan hanya memerlukan sertifikat Apostille dari Kemenkumham.</em></p>'
        ),
        "follow_up": ["Berapa biaya legalisasi di Kemenlu?", "Apa itu Apostille?", "Dokumen apa saja yang bisa dilegalisasi?"]
    },
    {
        "pattern": r"(syarat|prosedur|cara|membuat).*(visa).*(diplomatik|dinas)",
        "priority": 9,
        "context": "fasilitas diplomatik",
        "answer": (
            "<strong>Persyaratan Visa Diplomatik dan Dinas</strong>"
            "<p>Berikut adalah persyaratan umum untuk mengajukan permohonan Visa Diplomatik atau Visa Dinas ke Indonesia:</p>"
            "<ul>"
            "<li><strong>Permohonan Online:</strong> Wajib mengisi formulir dan mengunggah dokumen secara online melalui laman resmi di visa.kemlu.go.id.</li>"
            "<li><strong>Paspor Asli:</strong> Menyerahkan paspor diplomatik atau dinas yang masih berlaku minimal 6 bulan saat kedatangan.</li>"
            "<li><strong>Nota Diplomatik:</strong> Melampirkan nota diplomatik resmi dari kementerian luar negeri atau perwakilan negara pengirim.</li>"
            "<li><strong>Pas Foto:</strong> Menyerahkan 2 lembar pas foto berwarna terbaru (ukuran 4x6 cm) dengan latar belakang putih.</li>"
            "<li><strong>Tiket Perjalanan:</strong> Melampirkan salinan tiket atau rencana perjalanan (itinerary).</li>"
            "</ul>"
            "<p><em><strong>Penting:</strong> Persyaratan dapat sedikit berbeda di setiap Perwakilan RI. Sangat disarankan untuk memeriksa situs web Perwakilan RI tempat Anda akan mengajukan visa.</em></p>"
        ),
        "follow_up": ["Berapa lama proses pembuatan visa diplomatik?", "Apakah ada biaya untuk visa diplomatik?"]
    },
    {
        "pattern": r"kekonsuleran|layanan konsuler",
        "priority": 5,
        "context": "layanan konsuler",
        "answer": (
            '<strong>Layanan Kekonsuleran</strong>'
            '<p>Layanan kekonsuleran mencakup berbagai hal penting bagi WNI di luar negeri dan WNA yang berkepentingan dengan Indonesia. Beberapa layanan utama meliputi:</p>'
            '<ul>'
            '<li>Paspor dan SPLP</li>'
            '<li>Visa (Diplomatik, Dinas, Kunjungan)</li>'
            '<li>Legalisasi Dokumen</li>'
            '<li>Lapor Diri dan Pelindungan WNI</li>'
            '</ul>'
            '<p>Untuk informasi lebih detail, Anda dapat mengajukan pertanyaan yang lebih spesifik.</p>'
        ),
        "follow_up": ["Bagaimana cara perpanjang paspor?", "Apa syarat legalisasi dokumen?", "Bagaimana cara membuat visa kunjungan?"]
    },
    {
        "pattern": r"pelindungan wni|wni bermasalah|bantuan wni",
        "priority": 8,
        "context": "portal peduli wni|peduli wni",
        "answer": (
            '<strong>Layanan Pelindungan WNI</strong>'
            '<p>Kementerian Luar Negeri menyediakan layanan pelindungan bagi WNI di luar negeri melalui Perwakilan RI (KBRI/KJRI). Layanan ini mencakup bantuan dalam situasi darurat, masalah hukum, dan lainnya.</p>'
            '<ul>'
            '<li><strong>Portal Utama:</strong> Untuk lapor diri dan mendapatkan informasi, akses Portal Peduli WNI.</li>'
            '<li><strong>Aplikasi Mobile:</strong> Unduh aplikasi Safe Travel untuk informasi keamanan perjalanan dan notifikasi darurat.</li>'
            '<li><strong>Keadaan Darurat:</strong> Jika dalam keadaan darurat, segera hubungi Perwakilan RI terdekat di negara Anda.</li>'
            '</ul>'
        ),
        "follow_up": ["Bagaimana cara lapor diri online?", "Apa yang harus dilakukan jika paspor hilang?", "Bagaimana menghubungi KBRI terdekat dalam keadaan darurat?"]
    },
    {
        "pattern": r"fasilitas diplomatik|korps diplomatik",
        "priority": 7,
        "context": "fasilitas diplomatik",
        "answer": (
            '<strong>Layanan Fasilitas Diplomatik</strong>'
            '<p>Layanan ini ditujukan untuk memberikan kemudahan dan fasilitas kepada korps diplomatik, konsuler, serta organisasi internasional yang berada di Indonesia. Beberapa layanan utamanya adalah:</p>'
            '<ul>'
            '<li>Penerbitan ID Card untuk diplomat.</li>'
            '<li>Fasilitas untuk kendaraan bermotor.</li>'
            '<li>Fasilitas kepabeanan dan perpajakan.</li>'
            '</ul>'
            '<p>Informasi lengkap mengenai standar pelayanan dan produk layanan dapat diakses di halaman Fasilitas Diplomatik.</p>'
        ),
        "follow_up": ["Bagaimana cara mengajukan ID Card diplomatik?", "Apa saja fasilitas untuk kendaraan korps diplomatik?"]
    },
    {
        "pattern": r"kmiln|kartu masyarakat indonesia di luar negeri|diaspora card",
        "priority": 5,
        "context": "kartu masyarakat indonesia di luar negeri",
        "answer": 'Informasi lengkap tentang Kartu Masyarakat Indonesia di Luar Negeri (KMILN) atau Diaspora Card dapat diakses di halaman KMILN Kemlu.',
        "follow_up": ["Apa saja syarat membuat KMILN?", "Apa manfaat memiliki Diaspora Card?", "Bagaimana cara mendaftar?"]
    },
    {
        "pattern": r"pengaduan|lapor|sp4n",
        "priority": 5,
        "context": "pengaduan masyarakat",
        "answer": 'Untuk pengaduan masyarakat umum, silakan gunakan layanan SP4N LAPOR!. Kunjungi halaman pengaduan untuk informasi dan akses layanan.',
        "follow_up": ["Bagaimana cara membuat laporan di SP4N?", "Apakah identitas pelapor dijamin kerahasiaannya?"]
    },
    {
        "pattern": r"ppid|informasi publik",
        "priority": 5,
        "context": "ppid",
        "answer": 'Layanan Pejabat Pengelola Informasi dan Dokumentasi (PPID) untuk permohonan informasi publik tersedia di portal PPID Kemlu.',
        "follow_up": ["Bagaimana cara mengajukan permohonan informasi publik?", "Informasi apa saja yang bisa saya minta melalui PPID?"]
    },
    {
        "pattern": r"karir|lowongan kerja kemlu|rekrutmen asn",
        "priority": 3,
        "context": "karir",
        "answer": 'Informasi mengenai peluang karir dan rekrutmen di Kementerian Luar Negeri tersedia di halaman Karir.',
        "follow_up": ["Kapan pendaftaran diplomat dibuka?", "Apa saja persyaratan untuk menjadi diplomat?", "Bagaimana proses seleksinya?"]
    },
    {
        "pattern": r"perwakilan ri|daftar perwakilan",
        "priority": 3,
        "context": "perwakilan ri",
        "answer": (
            "<strong>Perwakilan Diplomatik Republik Indonesia</strong>"
            "<p>Diplomasi merupakan usaha memelihara hubungan antarnegara yang secara formal dilakukan oleh korps perwakilan diplomatik (dipimpin Duta Besar) dan korps perwakilan konsuler (dipimpin Konsul Jenderal). Konsulat berfokus pada hubungan antarmanusia dan ekonomi, tidak termasuk hubungan politik.</p>"
            "<p>Untuk mempererat hubungan dan kerjasama, Pemerintah Indonesia saat ini telah memiliki 132 perwakilan yang terdiri dari 95 Kedutaan Besar, 3 Perutusan Tetap (untuk PBB di New York dan Jenewa, serta ASEAN di Jakarta), 30 Konsulat Jenderal, dan 4 Konsulat. Selain itu, Indonesia juga telah mengangkat 64 Konsul Kehormatan.</p>"
            "<strong>Tugas dan Fungsi Utama Perwakilan RI:</strong>"
            "<ul>"
            "<li>Melaksanakan hubungan diplomatik dan/atau konsuler.</li>"
            "<li>Memperjuangkan kepentingan nasional Negara Republik Indonesia.</li>"
            "<li>Melindungi Warga Negara Indonesia (WNI) dan Badan Hukum Indonesia di wilayah akreditasi.</li>"
            "</ul>"
            "<p>Daftar lengkap seluruh Perwakilan RI dapat diakses di halaman Perwakilan.</p>"
        ),
        "follow_up": ["Di mana alamat KBRI terdekat?", "Apa beda kedutaan dan konsulat?", "Bagaimana cara menghubungi Konsulat Jenderal?"]
    },
    {
        "pattern": r"perwakilan asing|kedutaan asing|konsulat asing",
        "priority": 3,
        "context": "daftar perwakilan diplomatik dan konsuler asing",
        "answer": 'Daftar Perwakilan Diplomatik dan Konsuler Asing di Indonesia dapat ditemukan di halaman terkait di situs Kemlu.',
        "follow_up": ["Di mana alamat kedutaan besar negara sahabat?", "Bagaimana cara menghubungi konsulat asing?"]
    },
    {
        "pattern": r"berita|artikel terkini",
        "priority": 2,
        "context": "berita",
        "answer": 'Berita dan siaran pers terbaru dari Kementerian Luar Negeri dapat diakses di halaman Berita.',
        "follow_up": ["Di mana saya bisa menemukan siaran pers?", "Bagaimana cara berlangganan berita Kemlu?"]
    },
    {
        "pattern": r"kontak|hubungi kemlu",
        "priority": 1,
        "context": "kontak",
        "answer": 'Informasi kontak Kementerian Luar Negeri dapat ditemukan di halaman Kontak.',
        "follow_up": ["Apa alamat email resmi Kemlu?", "Berapa nomor telepon yang bisa dihubungi?"]
    },
    {
        "pattern": r"media sosial|sosmed",
        "priority": 1,
        "context": "media sosial",
        "answer": 'Ikuti akun media sosial resmi Kementerian Luar Negeri untuk mendapatkan informasi terbaru:<ul><li><strong>Instagram:</strong> @kemlu_ri</li><li><strong>X (Twitter):</strong> @Kemlu_RI</li><li><strong>Facebook:</strong> Kemlu.RI</li><li><strong>YouTube:</strong> MoFA Indonesia</li></ul>',
        "follow_up": ["Apakah Kemlu punya akun TikTok?", "Bagaimana cara mendapatkan update dari media sosial?"]
    },
]

# --- ENGLISH KEYWORDS (Mirrored from Indonesian for consistency) ---
KEYWORDS_EN = [
    {
        "pattern": r"self-report|register abroad",
        "priority": 10,
        "context": "lapor diri",
        "answer": (
            "<strong>Online Self-Reporting Procedure for Indonesian Citizens Abroad</strong>"
            "<p>Indonesian citizens residing abroad are strongly encouraged to self-report online through the Peduli WNI Portal. Here are the steps:</p>"
            "<strong>Online Self-Reporting Steps:</strong>"
            "<ul>"
            "<li>Visit the official site at: <a href='https://peduliwni.kemlu.go.id' target='_blank'>https://peduliwni.kemlu.go.id</a>.</li>"
            "<li><strong>Create an Account or Log In:</strong> If you don't have an account, please register first.</li>"
            "<li><strong>Fill Out the Form:</strong> Complete the Self-Report form with your personal data, passport information, address abroad, and emergency contacts.</li>"
            "<li><strong>Upload Documents:</strong> Prepare and upload supporting documents such as a copy of your passport and proof of residence permit (e.g., visa or local ID).</li>"
            "<li><strong>Save Proof:</strong> Once finished, make sure to save your self-reporting registration proof.</li>"
            "</ul>"
            "<strong>Benefits of Self-Reporting:</strong>"
            "<ul>"
            "<li>It helps Indonesian Missions (Embassies/Consulates) provide services and protection.</li>"
            "<li>It is a requirement for applying for various consular services.</li>"
            "</ul>"
        ),
        "follow_up": ["What documents need to be uploaded?", "Is self-reporting mandatory?", "How long does the verification process take?"]
    },
    {
        "pattern": r"(procedure|requirements|how to|renew|biometric|document).*(passport)",
        "priority": 10,
        "context": "consular services",
        "answer": (
            "<strong>Applying for or Renewing an Indonesian Passport</strong>"
            "<p>Here are the general steps and requirements for applying for or renewing an Indonesian passport:</p>"
            "<strong>General Steps:</strong>"
            "<ul>"
            "<li><strong>Schedule an Appointment Online:</strong> You generally need to book an appointment through the official website or app of the Immigration Office (if in Indonesia) or the Indonesian Mission (if abroad).</li>"
            "<li><strong>Visit the Location:</strong> Attend your scheduled appointment for data verification, photo-taking, and fingerprinting (biometrics).</li>"
            "<li><strong>Brief Interview:</strong> An officer will conduct a short interview for verification.</li>"
            "<li><strong>Make Payment:</strong> Pay the passport fee according to the applicable regulations.</li>"
            "</ul>"
            "<strong>Required Documents (Originals and Photocopies):</strong>"
            "<ul>"
            "<li>Valid <strong>E-KTP</strong> (Indonesian ID card).</li>"
            "<li><strong>Family Card (KK)</strong>.</li>"
            "<li><strong>One of the following:</strong> Birth Certificate, Diploma (elementary/middle/high school), or Marriage Certificate.</li>"
            "<li><strong>Old Passport:</strong> Mandatory if you are renewing your passport.</li>"
            "</ul>"
            "<p><em><strong>Important Note:</strong> Requirements abroad may differ slightly. Always check the website of the nearest Indonesian Mission for the most accurate information.</em></p>"
        ),
        "follow_up": ["How much does a passport cost?", "How long does the process take?", "What is the difference between a regular and an e-passport?"]
    },
    {
        "pattern": r"(requirements|procedure|how to|cost).*(legalization|legalize).*(document)",
        "priority": 9,
        "context": "document legalization",
        "answer": (
            '<strong>Document Legalization Services</strong>'
            '<p>Legalization is the process of authenticating the signature of an official and/or the official seal on a document. Here is general information based on common scenarios:</p>'
            '<strong>1. Legalization at Indonesian Missions (Embassy/Consulate)</strong>'
            '<p>This applies to documents issued abroad to be used in Indonesia, or vice versa. General requirements include:</p>'
            '<ul>'
            '<li><strong>Original Document:</strong> The document to be legalized.</li>'
            '<li><strong>Translation (if necessary):</strong> Documents in a foreign language must be translated into Indonesian by a sworn translator.</li>'
            '<li><strong>Identification:</strong> A photocopy of the applicant\'s passport or ID card.</li>'
            '<li><strong>Application Form:</strong> Filled out as provided by the Indonesian Mission.</li>'
            '<li><strong>Fee:</strong> Payment according to the applicable rates.</li>'
            '</ul>'
            '<strong>2. Legalization in Indonesia (for Use Abroad)</strong>'
            '<p>For documents issued in Indonesia to be used in other countries, the process is as follows:</p>'
            '<ol>'
            '<li><strong>Ministry of Law and Human Rights:</strong> The document must first be legalized at the Directorate of Civil Law.</li>'
            '<li><strong>Ministry of Foreign Affairs:</strong> After that, the document is legalized at the Directorate of Consular Affairs.</li>'
            '<li><strong>Embassy of the Destination Country:</strong> The final step is legalization at the Embassy or Consulate of the destination country in Jakarta.</li>'
            '</ol>'
            '<p><em><strong>Important Note:</strong> For countries that are members of the Apostille Convention, the process is simpler and only requires an Apostille certificate from the Ministry of Law and Human Rights.</em></p>'
        ),
        "follow_up": ["What is the legalization fee at the Ministry?", "What is an Apostille?", "What types of documents can be legalized?"]
    },
    {
        "pattern": r"consular|consular services",
        "priority": 5,
        "context": "consular services",
        "answer": (
            '<strong>Consular Services</strong>'
            '<p>Consular services cover various important matters for Indonesian citizens abroad and for foreign nationals with interests in Indonesia. Some of the main services include:</p>'
            '<ul>'
            '<li>Passport and Emergency Travel Document (SPLP)</li>'
            '<li>Visa (Diplomatic, Service, Visit)</li>'
            '<li>Document Legalization</li>'
            '<li>Self-Registration and Citizen Protection</li>'
            '</ul>'
            '<p>For more detailed information, you can ask a more specific question.</p>'
        ),
        "follow_up": ["How to renew a passport?", "What are the requirements for document legalization?", "How to apply for a visit visa?"]
    },
    {
        "pattern": r"citizen protection|wni issues|wni assistance",
        "priority": 8,
        "context": "citizen protection portal|peduli wni",
        "answer": (
            '<strong>Indonesian Citizen Protection Services</strong>'
            '<p>The Ministry of Foreign Affairs provides protection services for Indonesian citizens abroad through its Indonesian Missions (Embassies/Consulates). These services include assistance in emergencies, legal issues, and more.</p>'
            '<ul>'
            '<li><strong>Main Portal:</strong> For self-registration and information, access the <a href="https://peduliwni.kemlu.go.id/" target="_blank">Peduli WNI Portal</a>.</li>'
            '<li><strong>Mobile App:</strong> Download the Safe Travel application for travel security information and emergency notifications.</li>'
            '<li><strong>Emergencies:</strong> In an emergency, immediately contact the nearest <a href="https://kemlu.go.id/perwakilan" target="_blank">Indonesian Mission</a> in your country.</li>'
            '</ul>'
        ),
        "follow_up": ["How to self-report online?", "What to do if my passport is lost?", "How to contact the nearest embassy in an emergency?"]
    },
    {
        "pattern": r"career|job vacancy|recruitment",
        "priority": 3,
        "context": "career",
        "answer": 'Information about career opportunities and recruitment at the Ministry of Foreign Affairs is available on the Career page.',
        "follow_up": ["When does registration for diplomats open?", "What are the requirements to become a diplomat?", "What is the selection process like?"]
    },
    {
        "pattern": r"indonesian missions|list of missions|embassies list",
        "priority": 3,
        "context": "missions",
        "answer": (
            "<strong>Diplomatic Missions of the Republic of Indonesia</strong>"
            "<p>Diplomacy is the effort to maintain relations between countries, formally carried out by the diplomatic corps (led by an Ambassador) and the consular corps (led by a Consul General). A consulate focuses on human-to-human and economic relations, excluding political affairs.</p>"
            "<p>To strengthen relations and cooperation, the Indonesian Government currently has 132 missions, consisting of 95 Embassies, 3 Permanent Missions (to the UN in New York and Geneva, and to ASEAN in Jakarta), 30 Consulates General, and 4 Consulates. Additionally, Indonesia has appointed 64 Honorary Consuls.</p>"
            "<strong>Main Tasks and Functions of Indonesian Missions:</strong>"
            "<ul>"
            "<li>To conduct diplomatic and/or consular relations.</li>"
            "<li>To champion the national interests of the Republic of Indonesia.</li>"
            "<li>To protect Indonesian citizens and Indonesian legal entities in the accredited territory.</li>"
            "</ul>"
            "<p>A complete list of all Indonesian Missions can be accessed on the Missions page.</p>"
        ),
        "follow_up": ["Where is the nearest Indonesian Embassy?", "What is the difference between an embassy and a consulate?", "How do I contact the Consulate General?"]
    },
]

PERWAKILAN_DATA = {
    "Asia": {
        "afghanistan": {
            "name": "KBRI Kabul",
            "aliases": [],
            "link": "https://kemlu.go.id/kabul",
            "address": "Malalai Watt, Shah-re-Naw, Ministry of Interior Street, Kabul, Afghanistan",
            "wilayah_akreditasi": "Republik Islam Afghanistan",
            "telepon": "(93) 797-333-444 (Hotline)",
            "fax": None,
            "email": "kabul.kbri@kemlu.go.id",
            "website_detail": "https://kemlu.go.id/perwakilan/642e92efb79421734881b53e1e1b18b6?type=perwakilan-detail"
        },
        "arab saudi": {
            "name": "KBRI Riyadh",
            "aliases": ["saudi arabia"],
            "link": "https://kemlu.go.id/riyadh",
            "address": "Diplomatic Quarter, P.O. Box 94343 - Riyadh 11693",
            "wilayah_akreditasi": "Kerajaan Arab Saudi",
            "telepon": "(+966) 11 4882800",
            "fax": None,
            "email": "riyadh.kbri@kemlu.go.id",
            "website_detail": "https://kemlu.go.id/perwakilan/d1fe173d08e959397adf34b1d77e88d7?type=perwakilan-detail"
        },
        "jeddah": {
            "name": "KJRI Jeddah",
            "aliases": [],
            "link": "https://kemlu.go.id/jeddah",
            "address": "4653, Al-Muallifin Street, Al Rehab District/5, PO Box 10 Jeddah 23344, Jeddah, Kingdom of Saudi Arabia",
            "wilayah_akreditasi": "Gubernuran Tabuk, Madinah, Makkah, Assier, dan Organization of Islamic Cooperation (OIC)",
            "telepon": "+966 50 360 9667 / +966 12 671 1271",
            "fax": "Whatsapp: +966 50 596 6623",
            "email": "jeddah.kjri@kemlu.go.id",
            "website_detail": "https://kemlu.go.id/perwakilan/d9d4f495e875a2e075a1a4a6e1b9770f?type=perwakilan-detail"
        },
        "azerbaijan": {
            "name": "KBRI Baku",
            "aliases": [],
            "link": "https://kemlu.go.id/baku",
            "address": "4 Azer Aliyev, Nasimi District, Baku City, 1022, Azerbaijan",
            "wilayah_akreditasi": "Republik Azerbaijan",
            "telepon": "+994 12 597 05 14/596 21 68",
            "fax": "+994 12 596 21 68",
            "email": "baku.kbri@kemlu.go.id",
            "website_detail": "https://kemlu.go.id/perwakilan/6512bd43d9caa6e02c990b0a82652dca?type=perwakilan-detail"
        },
        "bahrain": {
            "name": "KBRI Manama",
            "aliases": [],
            "link": "https://kemlu.go.id/manama",
            "address": "Villa 2113, Road 2432, Block 324, Juffair, P.O. Box 75109 Manama, Kingdom of Bahrain",
            "wilayah_akreditasi": "Kerajaan Bahrain",
            "telepon": "+97317400164 & +97338791650 (Hotline)",
            "fax": "+973-1740 0267",
            "email": "manama.kbri@kemlu.go.id",
            "website_detail": "https://kemlu.go.id/perwakilan/72b32a1f754ba1c09b3695e0cb6cde7f?type=perwakilan-detail"
        },
        "bangladesh": {
            "name": "KBRI Dhaka",
            "aliases": [],
            "link": "https://kemlu.go.id/dhaka",
            "address": "Road No. 53, Plot No. 14, Gulshan-2 Dhaka-1212, Bangladesh.",
            "wilayah_akreditasi": "Merangkap Nepal",
            "telepon": "(+880) 2 58812260, 2 222281640, 2 222281641",
            "fax": None,
            "email": "dhaka.kbri@kemlu.go.id",
            "website_detail": "https://kemlu.go.id/perwakilan/a5bfc9e07964f8dddeb95fc584cd965d?type=perwakilan-detail"
        },
        "brunei darussalam": {
            "name": "KBRI Bandar Seri Begawan",
            "aliases": ["brunei"],
            "link": "https://kemlu.go.id/bandarseribegawan",
            "address": "Simpang 336, Diplomatic Enclave, Bandar Seri Begawan, Mukim Kianggeh, Brunei-Muara District, BA1210, Brunei",
            "wilayah_akreditasi": "Negara Brunei Darussalam",
            "telepon": "+673 233 0180",
            "fax": "+673 233 0646; 238 2489",
            "email": "bsbegawan.kbri@kemlu.go.id",
            "website_detail": "https://kemlu.go.id/perwakilan/c20ad4d76fe97759aa27a0c99bff6710?type=perwakilan-detail"
        },
        "china": {
            "name": "KBRI Beijing",
            "aliases": ["tiongkok"],
            "link": "https://kemlu.go.id/beijing",
            "address": "Dong Zhi Men Wai Da Jie No.4 Chaoyang District, Beijing 100600, Republik Rakyat Tiongkok",
            "wilayah_akreditasi": "Merangkap Mongolia",
            "telepon": "(86-10) 6532-5486, 6532-5488",
            "fax": "(86-10) 6532-5368",
            "email": "set.beijing.kbri@kemlu.go.id",
            "website_detail": "https://kemlu.go.id/perwakilan/aab3238922bcc25a6f606eb525ffdc56?type=perwakilan-detail"
        },
        "hongkong": {
            "name": "KJRI Hongkong",
            "aliases": [],
            "link": "https://kemlu.go.id/hongkong",
            "address": "127-129 Leighton Road, 6-8 Keswick Street, Causeway Bay Hong Kong, P. R. Tiongkok",
            "wilayah_akreditasi": "Wilayah administratif khusus Macao",
            "telepon": "(852) 3651 0200",
            "fax": "(852) 2895 0139",
            "email": "query@cgrihk.com",
            "website_detail": "https://kemlu.go.id/perwakilan/aab3238922bcc25a6f606eb525ffdc56?type=perwakilan-detail"
        },
        "guangzhou": {
            "name": "KJRI Guangzhou",
            "aliases": [],
            "link": "https://kemlu.go.id/guangzhou",
            "address": "38th floor of Atlas Center Plaza, No. one of 365, Tian He Bei Road, Tianhe District, Guangzhou, 510620",
            "wilayah_akreditasi": "Provinsi Guangdong, Fujian, Hainan, dan Guang Xi",
            "telepon": "(+86 20) 86018772",
            "fax": "(+86 20) 86018773",
            "email": "indonesiaguangzhou@kemlu.go.id",
            "website_detail": "https://kemlu.go.id/perwakilan/aab3238922bcc25a6f606eb525ffdc56?type=perwakilan-detail"
        },
        "shanghai": {
            "name": "KJRI Shanghai",
            "aliases": [],
            "link": "https://kemlu.go.id/shanghai",
            "address": "Shanghai Mart Building (Office Tower) 16/F Room 1611, Yan'an Road West No. 2299, Changning District, Shanghai 200336, Republik Rakyat Tiongkok",
            "wilayah_akreditasi": "Shanghai, Provinsi Jiangsu, Zhejiang, Anhui, dan Jiangxi",
            "telepon": "(86-21) 52402321*110, (86-21) 32516022",
            "fax": "(86-21) 32565627",
            "email": "kjrishanghai@kemlu.go.id",
            "website_detail": "https://kemlu.go.id/perwakilan/aab3238922bcc25a6f606eb525ffdc56?type=perwakilan-detail"
        },
        "filipina": {
            "name": "KBRI Manila",
            "aliases": ["philippines"],
            "link": "https://kemlu.go.id/manila",
            "address": "185 Salcedo Street, Legaspi Village, Makati City 1229 Metro Manila",
            "wilayah_akreditasi": "Merangkap Republik Kepulauan Marshall dan Republik Palau",
            "telepon": "+63 2 8892 5061 - 68, Hotline +63 954 158 3125",
            "fax": None,
            "email": "unitkom.manila@kemlu.go.id",
            "website_detail": "https://kemlu.go.id/perwakilan/1c383cd30b7c298ab50293adfecb7b18?type=perwakilan-detail"
        },
        "davao": {
            "name": "KJRI Davao City",
            "aliases": [],
            "link": "https://kemlu.go.id/davaocity",
            "address": "Phase IV, Ecoland Drive, Matina, 8000 Davao City, Philippines",
            "wilayah_akreditasi": "Seluruh Mindanao, Seluruh Sulu, dan Kelompok Kepulauan Tawi-Tawi",
            "telepon": "(63-82) 299-2930, Hotline: +63-966-2455-472",
            "fax": "(63-82) 297-0139",
            "email": "davao.kjri@kemlu.go.id",
            "website_detail": "https://kemlu.go.id/perwakilan/1c383cd30b7c298ab50293adfecb7b18?type=perwakilan-detail"
        },
        "india": {
            "name": "KBRI New Delhi",
            "aliases": [],
            "link": "https://kemlu.go.id/newdelhi",
            "address": "50-A Kautilya Marg, Chanakyapuri, New Delhi 110021",
            "wilayah_akreditasi": "Merangkap Kerajaan Bhutan",
            "telepon": "+91-11- 26118642-45",
            "fax": "+91-11-26874402, 26886763",
            "email": "newdelhi.kbri@kemlu.go.id",
            "website_detail": "https://kemlu.go.id/perwakilan/44f683a84163b3523afe57c2e008bc8c?type=perwakilan-detail"
        },
        "mumbai": {
            "name": "KJRI Mumbai",
            "aliases": [],
            "link": "https://kemlu.go.id/mumbai",
            "address": "19 Altamount Rd. Cumballa Hill Mumbai 400026 INDIA",
            "wilayah_akreditasi": "Negara Bagian Andhra Pradesh, Goa, Gujarat, Karnataka, Kerala, Maharasthra, Tamil Nadu, Telangana dan dua Wilayah Union yang terdiri atas Daman dan Diu, Puducherry.",
            "telepon": "+91 22 2351 1678/2353 0900/ 2353 0940",
            "fax": "+91 22 2351 0941/ 2351 5862",
            "email": "indonesia@kjrimumbai.net",
            "website_detail": "https://kemlu.go.id/perwakilan/44f683a84163b3523afe57c2e008bc8c?type=perwakilan-detail"
        },
        "irak": {
            "name": "KBRI Baghdad",
            "aliases": ["iraq"],
            "link": "https://kemlu.go.id/baghdad",
            "address": "Salhiya, Hay, Al-l'lam 220, Zukak 5, House 8 PO Box 420 Baghdad - Iraq",
            "wilayah_akreditasi": "Republik Irak",
            "telepon": "+964 776 984 2020",
            "fax": "(+964) 538-5155",
            "email": "baghdad.kbri@kemlu.go.id",
            "website_detail": "https://kemlu.go.id/perwakilan/d3d9446802a44259755d38e6d163e820?type=perwakilan-detail"
        },
        "iran": {
            "name": "KBRI Tehran",
            "aliases": [],
            "link": "https://kemlu.go.id/tehran",
            "address": "180, Ghaemmagham Farahani Ave. (P.O.BOX 11365/4564), Tehran, Iran",
            "wilayah_akreditasi": "Merangkap Turkmenistan",
            "telepon": "(98-21) 8871-6865, 8871-7251, 8855-3655, Hotline +98 99 1466 8845",
            "fax": "(98-21) 8871-8822",
            "email": "tehran.kbri@kemlu.go.id",
            "website_detail": "https://kemlu.go.id/perwakilan/8613985ec49eb8f757ae6439e879bb2a?type=perwakilan-detail"
        },
        "jepang": {
            "name": "KBRI Tokyo",
            "aliases": ["japan"],
            "link": "https://kemlu.go.id/tokyo",
            "address": "5-2-9 Higashigotanda, Shinagawa Ward, Tokyo 141-0022",
            "wilayah_akreditasi": "Merangkap Federasi Mikronesia",
            "telepon": "+81-03-3441-4201",
            "fax": "+81-03-3447-1697",
            "email": "info@kbritokyo.jp",
            "website_detail": "https://kemlu.go.id/perwakilan/3295c76acbf4caaed33c36b1b5fc2cb1?type=perwakilan-detail"
        },
        "osaka": {
            "name": "KJRI Osaka",
            "aliases": [],
            "link": "https://kemlu.go.id/osaka",
            "address": "Nakanoshima Intes Building 22 F, 6-2-40, Nakanoshima Kita-ku Osaka 530-0005 Japan",
            "wilayah_akreditasi": "Prefektur Fukui, Mie, Shiga, Kyoto, Osaka, Hyogo, Nara, Wakayama, Tottori, Shimane, Okayama, Hiroshima, Yamaguchi, Tokushima, Kagawa, Ehime, Kochi",
            "telepon": "(81-6) 6449-9898",
            "fax": "(81-6) 6449-9893, (81-6) 6449-9892",
            "email": "osaka.kjri@kemlu.go.id",
            "website_detail": "https://kemlu.go.id/perwakilan/3295c76acbf4caaed33c36b1b5fc2cb1?type=perwakilan-detail"
        },
        "jordania": {
            "name": "KBRI Amman",
            "aliases": ["jordan"],
            "link": "https://kemlu.go.id/amman",
            "address": "13 Ali Seedo Al-Kurdi Street, Sweifieh Amman",
            "wilayah_akreditasi": "Merangkap negara Palestina",
            "telepon": "(962-6) 5926908, 5926798",
            "fax": "+962 7791 50407",
            "email": "amman.kbri@kemlu.go.id",
            "website_detail": "https://kemlu.go.id/perwakilan/e4da3b7fbbce2345d7772b0674a318d5?type=perwakilan-detail"
        },
        "kamboja": {
            "name": "KBRI Phnom Penh",
            "aliases": ["cambodia"],
            "link": "https://kemlu.go.id/phnompenh",
            "address": "No. 33, Street 268, Preah Suramarit Boulevard, Phnom Penh, Kingdom of Cambodia",
            "wilayah_akreditasi": "Kerajaan Kamboja",
            "telepon": "+855 23 217 934, +855 23 216 148, +855 12 813 282",
            "fax": "+855 23 217 566",
            "email": "phnompenh.kbri@kemlu.go.id",
            "website_detail": "https://kemlu.go.id/perwakilan/e2c420d928d4bf8ce0ff2ec19b371514?type=perwakilan-detail"
        },
        "kazakhstan": {
            "name": "KBRI Astana",
            "aliases": [],
            "link": "https://kemlu.go.id/astana",
            "address": "22, улица Сарайшык, Esil district, Astana, 010000, Kazakhstan",
            "wilayah_akreditasi": "Merangkap Republik Tajikistan",
            "telepon": "+7 (7172) 79-06-70 , HOTLINE +7 771 836 0245",
            "fax": "+7 (7172) 79-06-73",
            "email": "astana.kbri@kemlu.go.id",
            "website_detail": "https://kemlu.go.id/perwakilan/c9f0f895fb98ab9159f51fd0297e236d?type=perwakilan-detail"
        },
        "korea selatan": {
            "name": "KBRI Seoul",
            "aliases": ["south korea", "korsel"],
            "link": "https://kemlu.go.id/seoul",
            "address": "380 Yeouidaebang-ro, Yeongdeungpo-gu, Seoul, Republik Korea 07342",
            "wilayah_akreditasi": "Republik Korea",
            "telepon": "02-2224 9000, 783 5675/7, Hotline (010-5394-2546)",
            "fax": "(+82)-02-7804280",
            "email": "seoul.kbri@kemlu.go.id",
            "website_detail": "https://kemlu.go.id/perwakilan/fe9fc289c3ff0af142b6d3bead98a923?type=perwakilan-detail"
        },
        "korea utara": {
            "name": "KBRI Pyongyang",
            "aliases": ["north korea", "korut"],
            "link": "https://kemlu.go.id/pyongyang",
            "address": "Foreigner's Building Munsudong Taedonggang Distric, Pyongyang, Republik Demokratik Rakyat Korea (P.O.BOX 178 PYONGYANG)",
            "wilayah_akreditasi": "Republik Rakyat Demokratik Korea",
            "telepon": "+850 2 3817425",
            "fax": "+850 2 3817620",
            "email": "pyongyang.kbri@kemlu.go.id",
            "website_detail": "https://kemlu.go.id/perwakilan/fbd7939d674997cdb4692d34de8633c4?type=perwakilan-detail"
        },
        "kuwait": {
            "name": "KBRI Kuwait City",
            "aliases": [],
            "link": "https://kemlu.go.id/kuwaitcity",
            "address": "9235+JWH, Rashid Bin Ahmad Al Roumi, Kuwait City",
            "wilayah_akreditasi": "Negara Kuwait",
            "telepon": "(+965) 2253 1021/25, Hotline: (+965) 9720 6060",
            "fax": "(+965) 2253 1024",
            "email": "kuwait.kbri@kemlu.go.id",
            "website_detail": "https://kemlu.go.id/perwakilan/2838023a778dfaecdc212708f721b788?type=perwakilan-detail"
        },
        "laos": {
            "name": "KBRI Vientiane",
            "aliases": [],
            "link": "https://kemlu.go.id/vientiane",
            "address": "Avenue Kaysone Phomvihane, Phonsa-At, Vientiane Capital, Xaysetha District, Vientiane Prefecture, 01009, Laos",
            "wilayah_akreditasi": "Republik Demokratik Rakyat Laos",
            "telepon": "(+856-21) 413 909, 413 900, 413 910",
            "fax": "(856-21) 214-828",
            "email": "vientiane.kbri@kemlu.go.id",
            "website_detail": "https://kemlu.go.id/perwakilan/f4b9ec30ad9f68f89b29639786cb62ef?type=perwakilan-detail"
        },
        "lebanon": {
            "name": "KBRI Beirut",
            "aliases": [],
            "link": "https://kemlu.go.id/beirut",
            "address": "Embassy of Indonesia, 806 Road, Hazmieh, Baabda, Baabda District, Mount Lebanon Governorate, 11072020, Lebanon",
            "wilayah_akreditasi": "Republik Lebanon",
            "telepon": "(+961) (5)924676",
            "fax": "(+961) (5) 924-678",
            "email": "beirut.kbri@kemlu.go.id",
            "website_detail": "https://kemlu.go.id/perwakilan/9bf31c7ff062936a96d3c8bd1f8f2ff3?type=perwakilan-detail"
        },
        "malaysia": {
            "name": "KBRI Kuala Lumpur",
            "aliases": [],
            "link": "https://kemlu.go.id/kualalumpur",
            "address": "233, Jalan Tun Razak. Imbi. 50400 Kuala Lumpur. Malaysia",
            "wilayah_akreditasi": "Malaysia",
            "telepon": "(603)-2116-4016 / 4017",
            "fax": "(603) 2141-7908, 2142-3878",
            "email": "kualalumpur.kbri@kemlu.go.id",
            "website_detail": "https://kemlu.go.id/perwakilan/67c6a1e7ce56d3d6fa748ab6d9af3fd7?type=perwakilan-detail"
        },
        "johor bahru": {
            "name": "KJRI Johor Bahru",
            "aliases": [],
            "link": "https://kemlu.go.id/johorbahru",
            "address": "No.46, Jl. Taat, Off Jalan Tun Abdul Razak 80100 Johor Bahru, Johor, Malaysia",
            "wilayah_akreditasi": "Johor, Melaka, Negeri Sembilan, Pahang",
            "telepon": "+60 7-227 4188/221 3241",
            "fax": "+60 7- 227 4288",
            "email": "johorbahru.kjri@kemlu.go.id",
            "website_detail": "https://kemlu.go.id/perwakilan/67c6a1e7ce56d3d6fa748ab6d9af3fd7?type=perwakilan-detail"
        },
        "kota kinabalu": {
            "name": "KJRI Kota Kinabalu",
            "aliases": [],
            "link": "https://kemlu.go.id/kotakinabalu",
            "address": "Lorong Kemajuan, Karamunsing P.O. Box 11595, 88100 Kota Kinabalu, Sabah, Malaysia",
            "wilayah_akreditasi": "Bagian Pantai Barat, Bagian Kudat, Bagian Pedalaman, Bagian Sandakan, dan Persekutuan Labuhan",
            "telepon": "088-219110, 088-218600",
            "fax": "(088) 215-170",
            "email": "kotakinabalu.kjri@kemlu.go.id",
            "website_detail": "https://kemlu.go.id/perwakilan/67c6a1e7ce56d3d6fa748ab6d9af3fd7?type=perwakilan-detail"
        },
        "kuching": {
            "name": "KJRI Kuching",
            "aliases": [],
            "link": "https://kemlu.go.id/kuching",
            "address": "Lot 86, Section 53, Jalan Central Timur, 93100 Kuching, Sarawak",
            "wilayah_akreditasi": "Negara Bagian Sarawak",
            "telepon": "+ (60)-82- 460734, 461734",
            "fax": "+(60)-82- 456734",
            "email": "kuching.kjri@kemlu.go.id",
            "website_detail": "https://kemlu.go.id/perwakilan/67c6a1e7ce56d3d6fa748ab6d9af3fd7?type=perwakilan-detail"
        },
        "penang": {
            "name": "KJRI Penang",
            "aliases": [],
            "link": "https://kemlu.go.id/penang",
            "address": "467, Jalan Burma Penang 10350",
            "wilayah_akreditasi": "Negara Bagian Kedah, Perlis, dan Pulau Penang",
            "telepon": "04-2274686 ; 04-2267412",
            "fax": None,
            "email": "penang.kjri@kemlu.go.id",
            "website_detail": "https://kemlu.go.id/perwakilan/67c6a1e7ce56d3d6fa748ab6d9af3fd7?type=perwakilan-detail"
        },
        "tawau": {
            "name": "KRI Tawau",
            "aliases": [],
            "link": "https://kemlu.go.id/tawau",
            "address": "TB 690-693 (LOT 5-8) Lorong Megah Jaya 10, Jalan Tiku KM 8, 91000 Tawau, Sabah-Malaysia.",
            "wilayah_akreditasi": "Tawau, Semporna, Kunak, dan Lahad Datu",
            "telepon": "(60-89) 772052 / 752969",
            "fax": "(60-89) 763859",
            "email": "tawau.kri@kemlu.go.id",
            "website_detail": "https://kemlu.go.id/perwakilan/67c6a1e7ce56d3d6fa748ab6d9af3fd7?type=perwakilan-detail"
        },
        "myanmar": {
            "name": "KBRI Yangon",
            "aliases": [],
            "link": "https://kemlu.go.id/yangon",
            "address": "No.100, Pyidaungsu Yeiktha Road, Dagon Township, Yangon",
            "wilayah_akreditasi": "Republik Uni Myanmar",
            "telepon": "(951) 254465, 254469, 229750",
            "fax": "(951) 254468",
            "email": "yangon.kbri@kemlu.go.id",
            "website_detail": "https://kemlu.go.id/perwakilan/ac627ab1ccbdb62ec96e702f07f6425b?type=perwakilan-detail"
        },
        "oman": {
            "name": "KBRI Muscat",
            "aliases": [],
            "link": "https://kemlu.go.id/muscat",
            "address": "Way 3048, Villa No. 3938 Al - Sarooj, Shati Al-Qurm Muscat, Sultanate of Oman",
            "wilayah_akreditasi": "Merangkap Republik Yaman",
            "telepon": "+968 2460 7000",
            "fax": "+968 2460 7070",
            "email": "muscat.kbri@kemlu.go.id",
            "website_detail": "https://kemlu.go.id/perwakilan/03afdbd66e7929b125f8597834fa83a4?type=perwakilan-detail"
        },
        "pakistan": {
            "name": "KBRI Islamabad",
            "aliases": [],
            "link": "https://kemlu.go.id/islamabad",
            "address": "Diplomatic Enclave I Street 5, Ramna G-5/4, Islamabad 44000, Pakistan (P.O.BOX 1019)",
            "wilayah_akreditasi": "Republik Islam Pakistan",
            "telepon": "(92-51) 283-2017 to 20",
            "fax": "(92-51) 835-8010",
            "email": "islamabad.kbri@kemlu.go.id",
            "website_detail": "https://kemlu.go.id/perwakilan/6c8349cc7260ae62e3b1396831a8398f?type=perwakilan-detail"
        },
        "karachi": {
            "name": "KJRI Karachi",
            "aliases": [],
            "link": "https://kemlu.go.id/karachi",
            "address": "E/1-5 Sharah - E-Iran, Clifton, Karachi 75600, Pakistan",
            "wilayah_akreditasi": "Provinsi Sindh",
            "telepon": "(92-21) 35874619",
            "fax": "(92- 21) 35874483",
            "email": "karachi.kjri@kemlu.go.id",
            "website_detail": "https://kemlu.go.id/perwakilan/6c8349cc7260ae62e3b1396831a8398f?type=perwakilan-detail"
        },
        "persatuan emirat arab": {
            "name": "KBRI Abu Dhabi",
            "aliases": ["pea", "uae", "uni emirat arab"],
            "link": "https://kemlu.go.id/abudhabi",
            "address": "Al Yaqout Street, Embassies District, Plot 42, Sector W59-02, Abu Dhabi, United Arab Emirates",
            "wilayah_akreditasi": "Persatuan Emirat Arab",
            "telepon": "(971-2) 445-4448",
            "fax": "(971-2) 445-5453",
            "email": "abudhabi.kbri@kemlu.go.id",
            "website_detail": "https://kemlu.go.id/perwakilan/c4ca4238a0b923820dcc509a6f75849b?type=perwakilan-detail"
        },
        "dubai": {
            "name": "KJRI Dubai",
            "aliases": [],
            "link": "https://kemlu.go.id/dubai",
            "address": "Al Hudaiba, Community 322, Villa No. 1, Bur Dubai, United Arab Emirates (P.O.BOX 73759)",
            "wilayah_akreditasi": "Wilayah Dubai, Sharjah, Fujairah, Ras Al Khaimah, Umm Al Quwain, dan Ajman",
            "telepon": "(971-4) 398-5666",
            "fax": "(971-4) 398-0804",
            "email": "dubai.kjri@kemlu.go.id",
            "website_detail": "https://kemlu.go.id/perwakilan/c4ca4238a0b923820dcc509a6f75849b?type=perwakilan-detail"
        },
        "ptri asean": {
            "name": "PTRI ASEAN",
            "aliases": [],
            "link": "https://kemlu.go.id/ptri-asean",
            "address": "Jl. Sisingamangaraja No. 73 Senayan, Jakarta Selatan 12120 Indonesia",
            "wilayah_akreditasi": "Merangkap Association of Southeast Asian Nations (ASEAN)",
            "telepon": "(62-21) 275 106 00",
            "fax": "(62-21) 291 263 24",
            "email": "amb.pr.indonesia@gmail.com",
            "website_detail": "https://kemlu.go.id/perwakilan/6974ce5ac660610b44d9b9fed0ff9548?type=perwakilan-detail"
        },
        "qatar": {
            "name": "KBRI Doha",
            "aliases": [],
            "link": "https://kemlu.go.id/doha",
            "address": "Al Salmiya Street No.21, Zone 66, Street 943, Onaiza, P.O. Box 22375, Doha",
            "wilayah_akreditasi": "Negara Qatar",
            "telepon": "+974-44657945, 44664981, 33322875 (Hotline)",
            "fax": "+974-44657610",
            "email": "doha.kbri@kemlu.go.id",
            "website_detail": "https://kemlu.go.id/perwakilan/d67d8ab4f4c10bf22aa353e27879133c?type=perwakilan-detail"
        },
        "singapura": {
            "name": "KBRI Singapura",
            "aliases": ["singapore"],
            "link": "https://kemlu.go.id/singapore",
            "address": "7 Chatsworth Road Singapore 249761",
            "wilayah_akreditasi": "Republik Singapura",
            "telepon": "(65) 6737 7422",
            "fax": "(65) 6737 5037/6235 5783",
            "email": "singapura.kbri@kemlu.go.id",
            "website_detail": "https://kemlu.go.id/perwakilan/68d30a9594728bc39aa24be94b319d21?type=perwakilan-detail"
        },
        "srilanka": {
            "name": "KBRI Colombo",
            "aliases": ["sri lanka"],
            "link": "https://kemlu.go.id/colombo",
            "address": "400/50 Sarana Road, Off Budhaloka Mawatha, Colombo 7, Sri Lanka",
            "wilayah_akreditasi": "Merangkap Republik Maladewa",
            "telepon": "(94-11) 267 43 37 / Hotline 1: +94 77 277 3123",
            "fax": "(94-11) 267 86 68/ Hotline 2: +94 76 884 8106",
            "email": "colombo.kbri@kemlu.go.id",
            "website_detail": "https://kemlu.go.id/perwakilan/c16a5320fa475530d9583c34fd356ef5?type=perwakilan-detail"
        },
        "suriah": {
            "name": "KBRI Damascus",
            "aliases": ["syria"],
            "link": "https://kemlu.go.id/Damascus",
            "address": "Mezzeh, Eastern Villas, al-Madina al-Munawara Street, opposite to Omar bin Abdul Aziz Mosque, Block 270/A Building No.26, P.O. Box: 3530, Damascus - SYRIA.",
            "wilayah_akreditasi": "Republik Arab Suriah",
            "telepon": "+963-11-6119630 / 31",
            "fax": "+963-11-6119632",
            "email": "damaskus.kbri@kemlu.go.id",
            "website_detail": "https://kemlu.go.id/perwakilan/182be0c5cdcd5072bb1864cdee4d3d6e?type=perwakilan-detail"
        },
        "taiwan": {
            "name": "KDEI Taipei",
            "aliases": [],
            "link": "https://kemlu.go.id/taipei",
            "address": "6F, No.550, Ruiguang Road, Neihu Dist., Taipei City 11492, Taiwan (R.O.C.)",
            "wilayah_akreditasi": "Taiwan",
            "telepon": None,
            "fax": None,
            "email": None,
            "website_detail": "https://kemlu.go.id/perwakilan/2a38a4a9316c49e5a833517c45d31070?type=perwakilan-detail"
        },
        "thailand": {
            "name": "KBRI Bangkok",
            "aliases": [],
            "link": "https://kemlu.go.id/bangkok",
            "address": "600-602 Petchburi Road Ratchatewi, Bangkok 10400, Thailand",
            "wilayah_akreditasi": "Economic and Social Commission for Asia and the Pacific (ESCAP)",
            "telepon": "(66-2) 2523135-40",
            "fax": "(66-2) 2551267",
            "email": "bangkok.kbri@kemlu.go.id",
            "website_detail": "https://kemlu.go.id/perwakilan/c51ce410c124a10e0db5e4b97fc2af39?type=perwakilan-detail"
        },
        "songkhla": {
            "name": "KRI Songkhla",
            "aliases": [],
            "link": "https://kemlu.go.id/songkhla",
            "address": "19 Sadao Road, Muang District, Songkhla 90000, Thailand",
            "wilayah_akreditasi": "Provinsi Songkhla, Krabi, Chumphon, Trang, Nakhon Si Thammarat, Narathiwat, Pattani, Yala, Phang-Nga, Phatthalung, Phuket, Ranong, Satun, dan Surat Thani",
            "telepon": "(66-74) 311-544, 312-219, 313-900",
            "fax": "(66-74) 313-905, 312-220",
            "email": "songkhla.kri@kemlu.go.id",
            "website_detail": "https://kemlu.go.id/perwakilan/c51ce410c124a10e0db5e4b97fc2af39?type=perwakilan-detail"
        },
        "timor leste": {
            "name": "KBRI Dili",
            "aliases": [],
            "link": "https://kemlu.go.id/dili",
            "address": "Rua Karketu Mota-Ain No. 2, Suco Motael, Sub Distrik Vera Cruz, Dili, Timor-Leste",
            "wilayah_akreditasi": "Republik Demokratik Timor Leste",
            "telepon": "(+670) 3317107, 3311109, 73755000 (hotline)",
            "fax": "(+670) 3323684",
            "email": "dili.kbri@kemlu.go.id",
            "website_detail": "https://kemlu.go.id/perwakilan/a5771bce93e200c36f7cd9dfd0e5deaa?type=perwakilan-detail"
        },
        "uzbekistan": {
            "name": "KBRI Tashkent",
            "aliases": [],
            "link": "https://kemlu.go.id/tashkent",
            "address": "73, Yahyo Gulomov Street, Tashkent 100000, Uzbekistan",
            "wilayah_akreditasi": "Merangkap Republik Kyrgyzstan",
            "telepon": "(998-71) 232-0236 to 38",
            "fax": "(998-71) 120-6540, 233-0513",
            "email": "unitkom@kbri-tashkent.go.id",
            "website_detail": "https://kemlu.go.id/perwakilan/7647966b7343c29048673252e490f736?type=perwakilan-detail"
        },
        "vietnam": {
            "name": "KBRI Hanoi",
            "aliases": [],
            "link": "https://kemlu.go.id/hanoi",
            "address": "50 Ngo Quyen Street , Hoan Kiem, Ha Noi, Viet Nam",
            "wilayah_akreditasi": "Republik Sosialis Vietnam",
            "telepon": "(+84-24) 3825-3353; (Citizen Hotline) +84705231990",
            "fax": "(+84-24) 3825-9274",
            "email": "hanoi.kbri@kemlu.go.id",
            "website_detail": "https://kemlu.go.id/perwakilan/d645920e395fedad7bbbed0eca3fe2e0?type=perwakilan-detail"
        },
        "ho chi minh": {
            "name": "KJRI Ho Chi Minh City",
            "aliases": [],
            "link": "https://kemlu.go.id/hochiminhcity",
            "address": "18 Phung Khac Khoan Street, Da Kao Ward, District 1, Ho Chi Minh City 77000, Vietnam",
            "wilayah_akreditasi": "Wilayah Southeast, Wilayah Mekong Delta, dan Sebagian Wilayah Central Highlands",
            "telepon": "Hotline: +84938730030. Visa: (84-28) 38251888/9, 38223799 ext 112 & 119",
            "fax": "(+84-28) 3829 9493, 3822 3839",
            "email": "hochiminh.kjri@kemlu.go.id",
            "website_detail": "https://kemlu.go.id/perwakilan/d645920e395fedad7bbbed0eca3fe2e0?type=perwakilan-detail"
        },
        "yaman": {
            "name": "KBRI Sana'a",
            "aliases": ["yemen"],
            "link": "https://kemlu.go.id/sanaa",
            "address": "Embassy of the Republic of Indonesia Faris Apartment 1, Unit 401-404, Way 25 No. 4, South Dahariz, Salalah - Oman",
            "wilayah_akreditasi": "Yaman",
            "telepon": "+968 9385 0979, 9611 4052",
            "fax": None,
            "email": "indosan@y.net.ye",
            "website_detail": "https://kemlu.go.id/perwakilan/ec8956637a99787bd197eacd77acce5e?type=perwakilan-detail"
        }
    },
    "Eropa": {
        "austria": {
            "name": "KBRI Wina",
            "aliases": [],
            "link": "https://kemlu.go.id/vienna",
            "address": "Gustav Tschermakgasse 5-7, A-1180, Wien, Austria",
            "wilayah_akreditasi": "Merangkap Republik Slovenia, United Nations Office at Vienna (UNOV)",
            "telepon": "+43147623 / Hotline +436763401946 (Emergency only)",
            "fax": "+4314730557",
            "email": "wina.kbri@kemlu.go.id",
            "website_detail": "https://kemlu.go.id/perwakilan/e2ef524fbf3d9fe611d5a8e90fefdc9c?type=perwakilan-detail"
        },
        "belanda": {
            "name": "KBRI Den Haag",
            "aliases": ["netherlands", "holland"],
            "link": "https://kemlu.go.id/denhaag",
            "address": "Tobias Asserlaan 8, 2517 KC - Den Haag, Belanda",
            "wilayah_akreditasi": "Merangkap Organization for the Prohibition of Chemical Weapons (OPCW)",
            "telepon": "(+31) 70 3108 100",
            "fax": "(+31) 62 88 60 509 (Emergency Hotline)",
            "email": "embassy@indonesia.nl",
            "website_detail": "https://kemlu.go.id/perwakilan/19ca14e7ea6328a42e0eb13d585e4c22?type=perwakilan-detail"
        },
        "belgia": {
            "name": "KBRI Brussels",
            "aliases": ["belgium"],
            "link": "https://kemlu.go.id/brussel",
            "address": "Boulevard de la Woluwe 38, 1200 Brussels, Belgium",
            "wilayah_akreditasi": "Merangkap Keharyapatihan Luksemburg, Uni Eropa, dan World Customs Organization (WCO)",
            "telepon": "Main: (32) 2 775 0120, Consular: (32) 2 771 2014",
            "fax": "(32) 2772-8210",
            "email": "kbri.brussel@skynet.be",
            "website_detail": "https://kemlu.go.id/perwakilan/b6d767d2f8ed5d21a44b0e5886680cb9?type=perwakilan-detail"
        },
        "bosnia and herzegovina": {
            "name": "KBRI Sarajevo",
            "aliases": ["bosnia"],
            "link": "https://kemlu.go.id/sarajevo",
            "address": "Splitska 9, 71000 Sarajevo Bosnia and Herzegovina",
            "wilayah_akreditasi": "Bosnia dan Herzegovina",
            "telepon": "+387 33 568510",
            "fax": "+387 33 568528",
            "email": "sarajevo.kbri@kemlu.go.id",
            "website_detail": "https://kemlu.go.id/perwakilan/9778d5d219c5080b9a6a17bef029331c?type=perwakilan-detail"
        },
        "bulgaria": {
            "name": "KBRI Sofia",
            "aliases": [],
            "link": "https://kemlu.go.id/sofia",
            "address": "Ulitsa Prof. Boyan Nichev 1A, 1434 Simeonovo, Sofia, Bulgaria. Akses depan: Ulitsa Simeonovska 18.",
            "wilayah_akreditasi": "Merangkap Republik Albania dan Republik Makedonia Utara",
            "telepon": "Tel: +359 9625240, 02 9057060, HOTLINE: +359 876445416",
            "fax": None,
            "email": "sofia.kbri@kemlu.go.id",
            "website_detail": "https://kemlu.go.id/perwakilan/3ef815416f775098fe977004015c6193?type=perwakilan-detail"
        },
        "ceko": {
            "name": "KBRI Praha",
            "aliases": ["czech republic"],
            "link": "https://kemlu.go.id/praha",
            "address": "Nad Budankami II 1944/ 7, 150 00, Praha 5 - Smichov, Republik Ceko",
            "wilayah_akreditasi": "Republik Ceko",
            "telepon": "+420 257 214 388",
            "fax": "+420 257 212 105",
            "email": "embassy@indonesia.cz",
            "website_detail": "https://kemlu.go.id/perwakilan/d2ddea18f00665ce8623e36bd4e3c7c5?type=perwakilan-detail"
        },
        "denmark": {
            "name": "KBRI Copenhagen",
            "aliases": [],
            "link": "https://kemlu.go.id/copenhagen",
            "address": "Ørehøj Alle 1, 2900 Hellerup, Denmark",
            "wilayah_akreditasi": "Denmark",
            "telepon": "+45 39 62 44 22",
            "fax": "+45 39 63 44 83",
            "email": "kopenhagen.kbri@kemlu.go.id",
            "website_detail": "https://kemlu.go.id/perwakilan/c0c7c76d30bd3dcaefc96f40275bdc0a?type=perwakilan-detail"
        },
        "finlandia": {
            "name": "KBRI Helsinki",
            "aliases": ["finland"],
            "link": "https://kemlu.go.id/helsinki",
            "address": "Kuusisaarentie 3, 00340 Helsinki, Finlandia",
            "wilayah_akreditasi": "Merangkap Republik Estonia",
            "telepon": "+358 (0) 9 4770370, +358 (0) 50 5167973 (Telp & WA)",
            "fax": "+358 (0) 9 4582882",
            "email": "helsinki.kbri@kemlu.go.id",
            "website_detail": "https://kemlu.go.id/perwakilan/17e62166fc8586dfa4d1bc0e1742c08b?type=perwakilan-detail"
        },
        "hungaria": {
            "name": "KBRI Budapest",
            "aliases": ["hungary"],
            "link": "https://kemlu.go.id/budapest",
            "address": "Városligeti fasor 26, 1068 Budapest, Hungary",
            "wilayah_akreditasi": "Republik Hungaria",
            "telepon": "(36-1) 41​​3-3800 to 01",
            "fax": "(36-1) 322-8669",
            "email": "budapest.kbri@kemlu.go.id",
            "website_detail": "https://kemlu.go.id/perwakilan/1ff1de774005f8da13f42943881c655f?type=perwakilan-detail"
        },
        "inggris": {
            "name": "KBRI London",
            "aliases": ["uk", "united kingdom", "britania raya"],
            "link": "https://kemlu.go.id/london",
            "address": "30 Great Peter Street, London SW1P 2BU, United Kingdom",
            "wilayah_akreditasi": "Merangkap Republik Irlandia dan International Maritime Organization (IMO)",
            "telepon": "(+44-20) 7290-9600",
            "fax": "(+44-20) 7491-4993",
            "email": "contact@indonesianembassy.org.uk",
            "website_detail": "https://kemlu.go.id/perwakilan/b53b3a3d6ab90ce0268229151c9bde11?type=perwakilan-detail"
        },
        "italia": {
            "name": "KBRI Roma",
            "aliases": ["italy"],
            "link": "https://kemlu.go.id/rome",
            "address": "Via Campania 55, 00187 Roma, Italia",
            "wilayah_akreditasi": "Merangkap Republik Malta, Republik San Marino, Republik Siprus, FAO, IFAD, WFP, dan UNIDROIT",
            "telepon": "+39064200911",
            "fax": "+39 06 4880280",
            "email": "roma.kbri@kemlu.go.id",
            "website_detail": "https://kemlu.go.id/perwakilan/f033ab37c30201f73f142449d037028d?type=perwakilan-detail"
        },
        "jerman": {
            "name": "KBRI Berlin",
            "aliases": ["germany"],
            "link": "https://kemlu.go.id/berlin",
            "address": "Clara-Wieck-Straße 1, Berlin 10785",
            "wilayah_akreditasi": "Republik Federal Jerman",
            "telepon": "+49 30 47807-200",
            "fax": "+49 30 44737142",
            "email": "query@indonesian-embassy.de",
            "website_detail": "https://kemlu.go.id/perwakilan/70efdf2ec9b086079795c442636b55fb?type=perwakilan-detail"
        },
        "frankfurt": {
            "name": "KJRI Frankfurt",
            "aliases": [],
            "link": "https://kemlu.go.id/frankfurt",
            "address": "23, Zeppelinallee, Bockenheim, Innenstadt 2, Frankfurt, Hesse, 60325, Germany",
            "wilayah_akreditasi": "Baden-Württemberg, Bayern, Hessen, Nordhein-Westfalen, Rheinland-Pfalz, dan Saarland",
            "telepon": "(+49-69) 247-0980",
            "fax": "(+49-69) 2470-9841",
            "email": "frankfurt.kjri@kemlu.go.id",
            "website_detail": "https://kemlu.go.id/perwakilan/70efdf2ec9b086079795c442636b55fb?type=perwakilan-detail"
        },
        "hamburg": {
            "name": "KJRI Hamburg",
            "aliases": [],
            "link": "https://kemlu.go.id/hamburg",
            "address": "Bebelallee 15, 22299 Hamburg, Germany",
            "wilayah_akreditasi": "Negara Bagian Schleswig-Holstein, Niedersachsen serta Kota Hamburg, dan Bremen",
            "telepon": "+49-(040) 51325711",
            "fax": "+49-(040) 5117531",
            "email": "info@kjrihamburg.de",
            "website_detail": "https://kemlu.go.id/perwakilan/70efdf2ec9b086079795c442636b55fb?type=perwakilan-detail"
        },
        "kroasia": {
            "name": "KBRI Zagreb",
            "aliases": ["croatia"],
            "link": "https://kemlu.go.id/zagreb",
            "address": "Medveščak 56, 10000 Zagreb",
            "wilayah_akreditasi": "Republik Kroasia",
            "telepon": "+38514578311​, +385995435372, +385994688444 (WNI)",
            "fax": "+38514578399",
            "email": "zagreb.kbri@kemlu.go.id",
            "website_detail": "https://kemlu.go.id/perwakilan/38b3eff8baf56627478ec76a704e9b52?type=perwakilan-detail"
        },
        "norwegia": {
            "name": "KBRI Oslo",
            "aliases": ["norway"],
            "link": "https://kemlu.go.id/oslo",
            "address": "Fritzners gate 12, PO. Box 4057 AMB, 0244 Oslo, Norway",
            "wilayah_akreditasi": "Merangkap Republik Islandia",
            "telepon": "+47 22 12 51 30, Hotline: +47 45 83 40 66",
            "fax": "+47 22 12 51 31",
            "email": "oslo.kbri@kemlu.go.id",
            "website_detail": "https://kemlu.go.id/perwakilan/735b90b4568125ed6c3f678819b6e058?type=perwakilan-detail"
        },
        "polandia": {
            "name": "KBRI Warsawa",
            "aliases": ["poland"],
            "link": "https://kemlu.go.id/warsawa",
            "address": "Ul. Estońska 3/5, 03-903 Warsaw, Poland",
            "wilayah_akreditasi": "Republik Polandia",
            "telepon": "+48 (22) 61 75 179",
            "fax": "+48 (22) 61 74 455",
            "email": "warsawa.kbri@kemlu.go.id",
            "website_detail": "https://kemlu.go.id/perwakilan/812b4ba287f5ee0bc9d43bbf5bbe87fb?type=perwakilan-detail"
        },
        "portugal": {
            "name": "KBRI Lisbon",
            "aliases": [],
            "link": "https://kemlu.go.id/lisbon",
            "address": "Avenida Dom Vasco da Gama no. 40, 1449-039, Belém, Lisboa, Portugal",
            "wilayah_akreditasi": "Republik Portugal",
            "telepon": "(+351) 210 159 999 / 965 595 687 / 961 710 010",
            "fax": "(351-21) 393-2079",
            "email": "lisabon.kbri@kemlu.go.id",
            "website_detail": "https://kemlu.go.id/perwakilan/a684eceee76fc522773286a895bc8436?type=perwakilan-detail"
        },
        "prancis": {
            "name": "KBRI Paris",
            "aliases": ["france"],
            "link": "https://kemlu.go.id/paris",
            "address": "47-49 rue Cortambert, 75116 Paris, France.",
            "wilayah_akreditasi": "Merangkap Kepangeranan Andorra, Kepangeranan Monako, dan UNESCO",
            "telepon": "+33 1 4503 0760",
            "fax": "+33 1 4070 7263",
            "email": "paris.kbri@kemlu.go.id",
            "website_detail": "https://kemlu.go.id/perwakilan/093f65e080a295f8076b1c5722a46aa2?type=perwakilan-detail"
        },
        "marseille": {
            "name": "KJRI Marseille",
            "aliases": [],
            "link": "https://kemlu.go.id/marseille",
            "address": "25 Boulevard Carmagnole, Marseille, Prancis",
            "wilayah_akreditasi": "Prancis Selatan",
            "telepon": "+33 491 23 01 60",
            "fax": "+33 491 23 01 62",
            "email": "marseille.kjri@kemlu.go.id",
            "website_detail": "https://kemlu.go.id/perwakilan/093f65e080a295f8076b1c5722a46aa2?type=perwakilan-detail"
        },
        "ptri jenewa": {
            "name": "PTRI Jenewa",
            "aliases": [],
            "link": "https://kemlu.go.id/jenewa",
            "address": "16 Rue de Saint-Jean, 1203 Geneva",
            "wilayah_akreditasi": "Untuk PBB, WTO, dan Organisasi Internasional Lainnya di Jenewa",
            "telepon": "+41 22 338 3350",
            "fax": "+41 22 345 5733",
            "email": "jenewa.ptri@kemlu.go.id",
            "website_detail": "https://kemlu.go.id/perwakilan/c9e1074f5b3f9fc8ea15d152add07294?type=perwakilan-detail"
        },
        "rumania": {
            "name": "KBRI Bucharest",
            "aliases": ["romania"],
            "link": "https://kemlu.go.id/bucharest",
            "address": "Strada Modrogan Nr.4, Sector 1, Bucharest, 011826, Romania",
            "wilayah_akreditasi": "Rumania",
            "telepon": "(40-21) 312 07 42; HOTLINE : +40 746 141 616",
            "fax": None,
            "email": "bucharest.kbri@kemlu.go.id",
            "website_detail": "https://kemlu.go.id/perwakilan/37693cfc748049e45d87b8c7d8b9aacd?type=perwakilan-detail"
        },
        "rusia": {
            "name": "KBRI Moscow",
            "aliases": ["russia"],
            "link": "https://kemlu.go.id/moscow",
            "address": "Novokuznetskaya Ulitsa No. 12, Moscow, Russian Federation, 119017",
            "wilayah_akreditasi": "Merangkap Republik Belarus",
            "telepon": "+7 (495) 951-9549 to 51",
            "fax": "+7 (495) 230-6431",
            "email": "moscow.kbri@kemlu.go.id",
            "website_detail": "https://kemlu.go.id/perwakilan/7f39f8317fbdb1988ef4c628eba02591?type=perwakilan-detail"
        },
        "serbia": {
            "name": "KBRI Belgrade",
            "aliases": [],
            "link": "https://kemlu.go.id/belgrade",
            "address": "Bulevar Kneza Aleksandra Karadjordjevica No. 18, Beograd, Serbia 11040, P.O. Box 559",
            "wilayah_akreditasi": "Merangkap Republik Montenegro",
            "telepon": "(+381-11) 3635 666",
            "fax": "(+381-11) 367 2984",
            "email": "beograd.kbri@kemlu.go.id",
            "website_detail": "https://kemlu.go.id/perwakilan/c74d97b01eae257e44aa9d5bade97baf?type=perwakilan-detail"
        },
        "slovakia": {
            "name": "KBRI Bratislava",
            "aliases": [],
            "link": "https://kemlu.go.id/bratislava",
            "address": "Brnianska 31, 811 04 Bratislava - Slovakia",
            "wilayah_akreditasi": "Republik Slowakia",
            "telepon": "+421-2-54419886",
            "fax": "+421-2-54419890",
            "email": "bratislava.kbri@kemlu.go.id",
            "website_detail": "https://kemlu.go.id/perwakilan/3c59dc048e8850243be8079a5c74d079?type=perwakilan-detail"
        },
        "spanyol": {
            "name": "KBRI Madrid",
            "aliases": ["spain"],
            "link": "https://kemlu.go.id/madrid",
            "address": "Calle de Agastia, 65, San Juan Bautista, Ciudad Lineal, Madrid, Comunidad de Madrid, 28043, España",
            "wilayah_akreditasi": "Merangkap United Nations World Tourism Organization (UNWTO)",
            "telepon": "+34 914 130 294, +34 914 130 594",
            "fax": "+34 914 138 994",
            "email": "madrid.kbri@kemlu.go.id",
            "website_detail": "https://kemlu.go.id/perwakilan/9f61408e3afb633e50cdf1b20de6f466?type=perwakilan-detail"
        },
        "swedia": {
            "name": "KBRI Stockholm",
            "aliases": ["sweden"],
            "link": "https://kemlu.go.id/stockholm",
            "address": "Kungsbroplan 1, 4 fl, (P.O.BOX 130 62) 112 27 Stockholm, Sweden",
            "wilayah_akreditasi": "Merangkap Republik Latvia",
            "telepon": "(46-8) 5455-5880",
            "fax": "(46-8) 650-8750",
            "email": "stockholm.kbri@kemlu.go.id",
            "website_detail": "https://kemlu.go.id/perwakilan/93db85ed909c13838ff95ccfa94cebd9?type=perwakilan-detail"
        },
        "swiss": {
            "name": "KBRI Bern",
            "aliases": ["switzerland"],
            "link": "https://kemlu.go.id/bern",
            "address": "Elfenauweg 51 3006 Bern, Switzerland",
            "wilayah_akreditasi": "Merangkap Kepangeranan Lichtenstein",
            "telepon": "+41 31 352 0983-85/ Hotline WNI: +41796533068",
            "fax": "+41 31 352 0984",
            "email": "bern.kbri@kemlu.go.id",
            "website_detail": "https://kemlu.go.id/perwakilan/6f4922f45568161a8cdf4ad2299f6d23?type=perwakilan-detail"
        },
        "turkiye": {
            "name": "KBRI Ankara",
            "aliases": ["turkey"],
            "link": "https://kemlu.go.id/ankara",
            "address": "Hilal Mh. Sukarno Cd. (Eski Hollanda Cd.) No.24/1 Cankaya 06550 Ankara / Türkiye",
            "wilayah_akreditasi": "Republik Türkiye",
            "telepon": "+90 312 969 73 54 - 56",
            "fax": "+90 312 969 73 36",
            "email": "ankara.kbri@kemlu.go.id",
            "website_detail": "https://kemlu.go.id/perwakilan/1679091c5a880faf6fb5e6087eb1b2dc?type=perwakilan-detail"
        },
        "istanbul": {
            "name": "KJRI Istanbul",
            "aliases": [],
            "link": "https://kemlu.go.id/istanbul",
            "address": "Dikilitaş Mah., Aşık Kerem Sokak, No.26, 34349 Beşiktaş - İstanbul, Turkiye",
            "wilayah_akreditasi": "Provinsi Istanbul, Tekirdağ, Edirne, Kirklareli, Kocaeli, Yalova, Bursa, Balikesir, dan Canakkale",
            "telepon": "+90 (212) 674-8686",
            "fax": "+90 (212) 674-8626",
            "email": "istanbul.kjri@kemlu.go.id",
            "website_detail": "https://kemlu.go.id/perwakilan/1679091c5a880faf6fb5e6087eb1b2dc?type=perwakilan-detail"
        },
        "ukraina": {
            "name": "KBRI Kyiv",
            "aliases": ["ukraine"],
            "link": "https://kemlu.go.id/kyiv",
            "address": "17 Universytetska Street, 03110, Kyiv, Ukraine",
            "wilayah_akreditasi": "Merangkap Republik Armenia dan Georgia",
            "telepon": "+380 44 3900 472, HOTLINE: +380 50 334 7917",
            "fax": None,
            "email": "kyiv.kbri@kemlu.go.id",
            "website_detail": "https://kemlu.go.id/perwakilan/9a1158154dfa42caddbd0694a4e9bdc8?type=perwakilan-detail"
        },
        "vatikan": {
            "name": "KBRI Takhta Suci Vatikan",
            "aliases": ["vatican"],
            "link": "https://kemlu.go.id/vatican",
            "address": "Via Marocco 10 00144 Roma – EUR Italia",
            "wilayah_akreditasi": "Takhta Suci Vatikan",
            "telepon": "+39 06 592 900 49 / 06 591 8610",
            "fax": "+39 06 542 212 92 / 06 542 104 49",
            "email": "vatican.kbri@kemlu.go.id",
            "website_detail": "https://kemlu.go.id/perwakilan/98dce83da57b0395e163467c9dae521b?type=perwakilan-detail"
        },
        "yunani": {
            "name": "KBRI Athena",
            "aliases": ["greece"],
            "link": "https://kemlu.go.id/athens",
            "address": "99, Marathonodromon Street, 15452 Paleo Psychico, Athens - Greece",
            "wilayah_akreditasi": "Republik Yunani",
            "telepon": "(210) 6774692, 6742345, 6746418",
            "fax": "(210) 6756955",
            "email": "athena.kbri@kemlu.go.id",
            "website_detail": "https://kemlu.go.id/perwakilan/45c48cce2e2d7fbdea1afc51c7c6ad26?type=perwakilan-detail"
        }
    },
    "Afrika": {
        "afrika selatan": {
            "name": "KBRI Pretoria",
            "aliases": ["south africa"],
            "link": "https://kemlu.go.id/pretoria",
            "address": "949 Francis Baard Street, Hatfield, Pretoria 0083",
            "wilayah_akreditasi": "Merangkap Republik Botswana, Kerajaan Lesotho, dan Kerajaan Eswatini",
            "telepon": "+27 123423350 - 123423353",
            "fax": "+27123423369",
            "email": "pretoria.kbri@kemlu.go.id",
            "website_detail": "https://kemlu.go.id/perwakilan/33e75ff09dd601bbe69f351039152189?type=perwakilan-detail"
        },
        "cape town": {
            "name": "KJRI Cape Town",
            "aliases": [],
            "link": "https://kemlu.go.id/capetown",
            "address": "124 Rosmead Avenue, Kenilworth 7708 Cape Town, South Africa",
            "wilayah_akreditasi": "Provinsi Northern Cape, Western Cape, Eastern Cape, dan Free State",
            "telepon": "+27 21 761 7015 | +27727116760 (Hotline Perlindungan WNI, Khusus Keadaan Darurat)",
            "fax": None,
            "email": "indo.capetown@kemlu.go.id",
            "website_detail": "https://kemlu.go.id/perwakilan/33e75ff09dd601bbe69f351039152189?type=perwakilan-detail"
        },
        "aljazair": {
            "name": "KBRI Algiers",
            "aliases": ["algeria"],
            "link": "https://kemlu.go.id/algiers",
            "address": "Villa No. 17, Domaine Chekiken, Ex-Rue De La Madeleine, Ben Aknoun, Alger, Aljazair",
            "wilayah_akreditasi": "Republik Demokratik Rakyat Aljazair",
            "telepon": "+213-23-473877",
            "fax": "+213-23-473817",
            "email": "alger.kbri@kemlu.go.id",
            "website_detail": "https://kemlu.go.id/perwakilan/a87ff679a2f3e71d9181a67b7542122c?type=perwakilan-detail"
        },
        "ethiopia": {
            "name": "KBRI Addis Ababa",
            "aliases": [],
            "link": "https://kemlu.go.id/addisababa",
            "address": "Nifas Silk Lafto Subcity, Egypt Street, Woreda 05, House No. 1816 PO Box 1004, Addis Ababa",
            "wilayah_akreditasi": "Merangkap Republik Djibouti, Negara Eritrea",
            "telepon": "+251 113 71 01 21 Hotline : +251 92 990 1406",
            "fax": "011 371 0873",
            "email": "addisababa.kbri@kemlu.go.id",
            "website_detail": "https://kemlu.go.id/perwakilan/eccbc87e4b5ce2fe28308fd9f2a7baf3?type=perwakilan-detail"
        },
        "kamerun": {
            "name": "KBRI Yaounde",
            "aliases": ["cameroon"],
            "link": "https://kemlu.go.id/yaounde",
            "address": "Rue 1793, B.P. 35330, Nouvelle Bastos, Yaoundé, Cameroon",
            "wilayah_akreditasi": "Merangkap Chad, Republik Afrika Tengah, Republik Kongo, Guinea Ekuatorial, dan Gabon",
            "telepon": "+237 682210679",
            "fax": None,
            "email": "yaounde.kbri@kemlu.go.id",
            "website_detail": "https://kemlu.go.id/perwakilan/f899139df5e1059396431415e770c6dd?type=perwakilan-detail"
        },
        "kenya": {
            "name": "KBRI Nairobi",
            "aliases": [],
            "link": "https://kemlu.go.id/nairobi",
            "address": "Menengai Rd, Upper Hill, Nairobi P.O. Box 48868 Kenya",
            "wilayah_akreditasi": "Merangkap Republik Demokratik Kongo, Republik Federal Somalia, Republik Uganda",
            "telepon": "+254 (0)20 2714196 / +254 (0)20 2714197",
            "fax": "+254 20 713475",
            "email": "nairobi.kbri@kemlu.go.id",
            "website_detail": "https://kemlu.go.id/perwakilan/ea5d2f1c4608232e07d3aa3d998e5135?type=perwakilan-detail"
        },
        "libya": {
            "name": "KBRI Tripoli",
            "aliases": [],
            "link": "https://kemlu.go.id/tripoli",
            "address": "Hay Al Karamah, Qobri Taariq Al Sari', Amaama Al Saraaj, (P.O.BOX 5921) Tripoli, Libya",
            "wilayah_akreditasi": "Negara Libya",
            "telepon": "+218 94-4815608",
            "fax": None,
            "email": "tripoli.kbri@kemlu.go.id",
            "website_detail": "https://kemlu.go.id/perwakilan/54229abfcfa5649e7003b83dd4755294?type=perwakilan-detail"
        },
        "madagaskar": {
            "name": "KBRI Antananarivo",
            "aliases": ["madagascar"],
            "link": "https://kemlu.go.id/antananarivo",
            "address": "Lot II J Ter A Ivandry Antananarivo 101",
            "wilayah_akreditasi": "Merangkap Republik Mauritius, Republik Seychelles, dan Uni Komoro",
            "telepon": "(261-20) 23 249 15, 23 336 77, 23 660 96 ext. 119",
            "fax": "(261-20) 23 323 15",
            "email": "antananarivo.kbri@kemlu.go.id",
            "website_detail": "https://kemlu.go.id/perwakilan/8f14e45fceea167a5a36dedd4bea2543?type=perwakilan-detail"
        },
        "maroko": {
            "name": "KBRI Rabat",
            "aliases": ["morocco"],
            "link": "https://kemlu.go.id/rabat",
            "address": "63 Rue Beni Boufrah Routes des Zaers km 6, Souissi - Rabat 10000, Morocco.",
            "wilayah_akreditasi": "Merangkap Republik Islam Mauritania",
            "telepon": "(+212) 537 - 75 78 60/61",
            "fax": "(+212) 537 - 75 78 59",
            "email": "rabat.kbri@kemlu.go.id",
            "website_detail": "https://kemlu.go.id/perwakilan/35f4a8d465e6e1edc05f3d8ab658c551?type=perwakilan-detail"
        },
        "mesir": {
            "name": "KBRI Kairo",
            "aliases": ["egypt"],
            "link": "https://kemlu.go.id/cairo",
            "address": "13, Aisha El Taymouria Street, Garden City, Cairo, Arab Republic of Egypt",
            "wilayah_akreditasi": "Republik Arab Mesir",
            "telepon": "+202-24715561",
            "fax": "+202-27900068",
            "email": "info@kbri-cairo.org",
            "website_detail": "https://kemlu.go.id/perwakilan/4e732ced3463d06de0ca9a15b6153677?type=perwakilan-detail"
        },
        "mozambique": {
            "name": "KBRI Maputo",
            "aliases": ["mozambik"],
            "link": "https://kemlu.go.id/maputo",
            "address": "Jalan Dar Es Salaam No. 141, Sommerschield 1102 Maputo, Mozambique",
            "wilayah_akreditasi": "Merangkap Republik Malawi",
            "telepon": "(+258) 21494227/21494228/21494229",
            "fax": "+258 21 494231",
            "email": "maputo.kbri@kemlu.go.id",
            "website_detail": "https://kemlu.go.id/perwakilan/66f041e16a60928b05a7e228a89c3799?type=perwakilan-detail"
        },
        "namibia": {
            "name": "KBRI Windhoek",
            "aliases": [],
            "link": "https://kemlu.go.id/windhoek",
            "address": "103, Nelson Mandela Avenue, Windhoek, Namibia (P.O.BOX 20691 Whk)",
            "wilayah_akreditasi": "Merangkap Republik Angola",
            "telepon": "+264612851000 hotline +264811249745, +264857378919",
            "fax": "(+264-61) 285-1231",
            "email": "windhoek.kbri@kemlu.go.id",
            "website_detail": "https://kemlu.go.id/perwakilan/ed3d2c21991e3bef5e069713af9fa6ca?type=perwakilan-detail"
        },
        "nigeria": {
            "name": "KBRI Abuja",
            "aliases": [],
            "link": "https://kemlu.go.id/abuja",
            "address": "10 Katsina Ala Crescent, Maitama District, Abuja FCT Nigeria",
            "wilayah_akreditasi": "Merangkap Benin, Burkina Faso, Ghana, Liberia, Niger, Sao Tome dan Principe, Togo, serta ECOWAS",
            "telepon": "(+234 8166026466)",
            "fax": None,
            "email": "abuja.kbri@kemlu.go.id",
            "website_detail": "https://kemlu.go.id/perwakilan/c81e728d9d4c2f636f067f89cc14862c?type=perwakilan-detail"
        },
        "senegal": {
            "name": "KBRI Dakar",
            "aliases": [],
            "link": "https://kemlu.go.id/dakar",
            "address": "Avenue Cheikh Anta Diop, Commune de Mermoz-Sacré-Cœur, Arrondissement des Almadies, Dakar, Dakar Region, 15150, Senegal",
            "wilayah_akreditasi": "Merangkap Gambia, Guinea-Bissau, Guinea, Sierra Leone, Pantai Gading, Mali, dan Cabo Verde",
            "telepon": "(221) 33 825-7316, 33 824-0738",
            "fax": "(221) 33 825-5896",
            "email": "dakar.kbri@kemlu.go.id",
            "website_detail": "https://kemlu.go.id/perwakilan/6364d3f0f495b6ab9dcf8d3b5c6e0b01?type=perwakilan-detail"
        },
        "sudan": {
            "name": "KBRI Khartoum",
            "aliases": [],
            "link": "https://kemlu.go.id/khartoum",
            "address": "Hay Matar Qadim Block 20, No. 448, Port Sudan, Red Sea - Sudan",
            "wilayah_akreditasi": "Republik Sudan",
            "telepon": "(+249) 90 797 8701",
            "fax": "(+249) 90 007 9050 (WhatsApp)",
            "email": "khartoum.kbri@kemlu.go.id",
            "website_detail": "https://kemlu.go.id/perwakilan/f457c545a9ded88f18ecee47145a72c0?type=perwakilan-detail"
        },
        "tanzania": {
            "name": "KBRI Dar es Salaam",
            "aliases": [],
            "link": "https://kemlu.go.id/daressalaam",
            "address": "299 Ali Hassan Mwinyi Road, (P.O.BOX 572) Dar es Salaam, Tanzania",
            "wilayah_akreditasi": "Merangkap Tanzania, Republik Burundi dan Republik Rwanda",
            "telepon": "(255-22) 211-8133, 211-5841. +255 22 2119119",
            "fax": "255 22 2115849",
            "email": "daressalaam.kbri@kemlu.go.id",
            "website_detail": "https://kemlu.go.id/perwakilan/e369853df766fa44e1ed0ff613f563bd?type=perwakilan-detail"
        },
        "tunisia": {
            "name": "KBRI Tunis",
            "aliases": [],
            "link": "https://kemlu.go.id/tunis",
            "address": "15, Rue du Lac Mälaren, Les berges du Lac, (BP. 58 Les Berges du Lac, 1053) Tunis, Tunisia",
            "wilayah_akreditasi": "Republik Tunisia",
            "telepon": "(+216) 71860377 ; 71860702 ; 71963973",
            "fax": "(+216) 71861758",
            "email": "kbritun@gnet.tn",
            "website_detail": "https://kemlu.go.id/perwakilan/92cc227532d17e56e07902b254dfad10?type=perwakilan-detail"
        },
        "zimbabwe": {
            "name": "KBRI Harare",
            "aliases": [],
            "link": "https://kemlu.go.id/harare",
            "address": "3 Duthie Avenue, P.O.Box 69 CY Causeway, Harare, Zimbabwe",
            "wilayah_akreditasi": "Merangkap Republik Zambia",
            "telepon": "(+263-24) 2251 799 / 2250 072 / hotline : +263 783 419111",
            "fax": "(+263 24) 2796 587",
            "email": "harare.kbri@kemlu.go.id",
            "website_detail": "https://kemlu.go.id/perwakilan/3416a75f4cea9109507cacd8e2f2aefc?type=perwakilan-detail"
        }
    },
    "Amerika": {
        "amerika serikat": {
            "name": "KBRI Washington D.C.",
            "aliases": ["usa", "united states", "as"],
            "link": "https://kemlu.go.id/washington",
            "address": "2020 Massachusetts Avenue NW, Washington, D.C. 20036",
            "wilayah_akreditasi": "Amerika Serikat",
            "telepon": "+1 (202) 775 5200",
            "fax": "+1 (202) 775 5236",
            "email": "washington.kbri@kemlu.go.id",
            "website_detail": "https://kemlu.go.id/perwakilan/34173cb38f07f89ddbebc2ac9128303f?type=perwakilan-detail"
        },
        "chicago": {
            "name": "KJRI Chicago",
            "aliases": [],
            "link": "https://kemlu.go.id/chicago",
            "address": "211 North Carpenter St Chicago, Illinois, 60607",
            "wilayah_akreditasi": "Negara Bagian Illinois, Michigan, Wisconsin, Indiana, Iowa, Kansas, Minnesota, Missouri, Nebraska, North Dakota, South Dakota, Kentucky, dan Ohio",
            "telepon": "+1-312-920-1880",
            "fax": "1-312-920-1881",
            "email": "consular@indonesiachicago.org",
            "website_detail": "https://kemlu.go.id/perwakilan/34173cb38f07f89ddbebc2ac9128303f?type=perwakilan-detail"
        },
        "houston": {
            "name": "KJRI Houston",
            "aliases": [],
            "link": "https://kemlu.go.id/houston",
            "address": "10900 Richmond Avenue, Houston, Texas 77042, Amerika Serikat",
            "wilayah_akreditasi": "Negara Bagian New Mexico, Texas, Oklahoma, Arkansas, Tennessee, Mississippi, Louisiana, Alabama, Georgia, Florida, United States Virgin Islands, dan The Commonwealth of Puerto Rico",
            "telepon": "(1-713) 785-1691",
            "fax": "(1-713) 780-9644",
            "email": "info@indonesiahouston.net",
            "website_detail": "https://kemlu.go.id/perwakilan/34173cb38f07f89ddbebc2ac9128303f?type=perwakilan-detail"
        },
        "los angeles": {
            "name": "KJRI Los Angeles",
            "aliases": [],
            "link": "https://kemlu.go.id/losangeles",
            "address": "3457 Wilshire blvd, Los Angeles, CA 90010.",
            "wilayah_akreditasi": "Negara Bagian Arizona, Colorado, Hawaii, Utah, Nevada sebelah selatan, Negara Bagian California sebelah selatan, dan Daerah di Kepulauan Pasifik yang berada di bawah pemerintahan Amerika Serikat",
            "telepon": "(213) 383-5126, (213) 383-5127",
            "fax": None,
            "email": "losangeles.kjri@kemlu.go.id",
            "website_detail": "https://kemlu.go.id/perwakilan/34173cb38f07f89ddbebc2ac9128303f?type=perwakilan-detail"
        },
        "new york": {
            "name": "KJRI New York",
            "aliases": [],
            "link": "https://kemlu.go.id/newyork",
            "address": "5, East 68th Street, New York, NY 10065, The United States of America",
            "wilayah_akreditasi": "Negara Bagian Connecticut, Delaware, Maryland, Maine, Massachusetts, New Hampshire, New Jersey, New York, North Carolina, South Carolina, Pennsylvania, Rhode Island, Vermont, Virginia, dan West Virginia",
            "telepon": "(+1-212) 879-0601 to 604",
            "fax": "(1-212) 570-6206",
            "email": "information.newyork@kemlu.go.id",
            "website_detail": "https://kemlu.go.id/perwakilan/34173cb38f07f89ddbebc2ac9128303f?type=perwakilan-detail"
        },
        "ptri new york": {
            "name": "PTRI New York",
            "aliases": [],
            "link": "https://kemlu.go.id/newyork-un",
            "address": "325 East 38th Street, New York, NY, 10016, USA",
            "wilayah_akreditasi": "Merangkap Perserikatan Bangsa-Bangsa dan Organisasi Internasional Lainnya di New York, dan International Seabed Authority (ISA)",
            "telepon": "+1-212-972-8333",
            "fax": "+1-212-972-9780",
            "email": "ptri@indonesiaun.org",
            "website_detail": "https://kemlu.go.id/perwakilan/34173cb38f07f89ddbebc2ac9128303f?type=perwakilan-detail"
        },
        "san francisco": {
            "name": "KJRI San Francisco",
            "aliases": [],
            "link": "https://kemlu.go.id/sanfrancisco",
            "address": "1111 Columbus Ave, San Francisco, CA 94133.",
            "wilayah_akreditasi": "Negara Bagian Alaska, Idaho, Montana, Oregon, Washington State, Wyoming, Nevada sebelah utara, California sebelah utara",
            "telepon": "+1 (415) 474 9571 | Bagian Konsuler: +1 (415) 432-9498",
            "fax": "+1 (415) 441-4320",
            "email": "konsuler@kjrisfo.net",
            "website_detail": "https://kemlu.go.id/perwakilan/34173cb38f07f89ddbebc2ac9128303f?type=perwakilan-detail"
        },
        "argentina": {
            "name": "KBRI Buenos Aires",
            "aliases": [],
            "link": "https://kemlu.go.id/buenosaires",
            "address": "Mariscal Ramon Castilla 2901, 1425 Capital Federal Buenos Aires, Argentina",
            "wilayah_akreditasi": "Merangkap Republik Paraguay dan Republik Oriental Uruguay",
            "telepon": "( 5411 ) 4807-2211, 4807-2956, 4807-3324",
            "fax": "( 5411 ) 4802-4448",
            "email": "buenosaires.kbri@kemlu.go.id",
            "website_detail": "https://kemlu.go.id/perwakilan/8e296a067a37563370ded05f5a3bf3ec?type=perwakilan-detail"
        },
        "brazil": {
            "name": "KBRI Brasilia",
            "aliases": ["brasil"],
            "link": "https://kemlu.go.id/brasilia",
            "address": "SES Avenida Das Nacoes Quadra 805, Lote. 20 CEP-70479-900 Brasilia-DF, Brazilia",
            "wilayah_akreditasi": "Republik Federasi Brasil",
            "telepon": "(55-61) 3443-8800, 3443-1788, 99529-6775",
            "fax": "(55-61) 3443-6732",
            "email": "brasilia.kbri@kemlu.go.id",
            "website_detail": "https://kemlu.go.id/perwakilan/98f13708210194c475687be6106a3b84?type=perwakilan-detail"
        },
        "chile": {
            "name": "KBRI Santiago",
            "aliases": ["chili"],
            "link": "https://kemlu.go.id/santiago",
            "address": "Av. Las Urbinas 160, Providencia, Santiago, Chile",
            "wilayah_akreditasi": "Republik Chile",
            "telepon": "+56 2 2207 7623, +56 9 9827 7292",
            "fax": "(+56) 998 277 292",
            "email": "santiago.kbri@kemlu.go.id",
            "website_detail": "https://kemlu.go.id/perwakilan/43ec517d68b6edd3015b3edc9a11367b?type=perwakilan-detail"
        },
        "ecuador": {
            "name": "KBRI Quito",
            "aliases": ["ekuador"],
            "link": "https://kemlu.go.id/quito",
            "address": "CALLE QUITEÑO LIBRE E15-84 Y LA CUMBRE, BELLAVISTA QUITO, ECUADOR.",
            "wilayah_akreditasi": "Republik Ekuador",
            "telepon": "+593-2-2431717",
            "fax": "+59322923544",
            "email": "quito.kbri@kemlu.go.id",
            "website_detail": "https://kemlu.go.id/perwakilan/28dd2c7955ce926456240b2ff0100bde?type=perwakilan-detail"
        },
        "kanada": {
            "name": "KBRI Ottawa",
            "aliases": ["canada"],
            "link": "https://kemlu.go.id/ottawa",
            "address": "55 Parkdale Avenue, Ottawa, ON K1Y 1E5 Kanada",
            "wilayah_akreditasi": "Merangkap International Civil Aviation Organization (ICAO)",
            "telepon": "(1-613) 724-1100",
            "fax": "(1-613) 724-1105",
            "email": "publicaffairs@indonesia-ottawa.org",
            "website_detail": "https://kemlu.go.id/perwakilan/a3f390d88e4c41f2747bfa2f1b5f87db?type=perwakilan-detail"
        },
        "toronto": {
            "name": "KJRI Toronto",
            "aliases": [],
            "link": "https://kemlu.go.id/toronto",
            "address": "129 Jarvis Street, Toronto Ontario, M5C 2H6",
            "wilayah_akreditasi": "Provinsi Manitoba, Ontario, Saskatchewan, dan wilayah Nunavut",
            "telepon": "(416) 360-4020",
            "fax": "(416) 360-4295",
            "email": "admin@indonesiatoronto.org",
            "website_detail": "https://kemlu.go.id/perwakilan/a3f390d88e4c41f2747bfa2f1b5f87db?type=perwakilan-detail"
        },
        "vancouver": {
            "name": "KJRI Vancouver",
            "aliases": [],
            "link": "https://kemlu.go.id/vancouver",
            "address": "1630 Alberni Street, Vancouver, British Columbia, Kanada V6G 1A6",
            "wilayah_akreditasi": "Provinsi British Columbia, Alberta, Yukon, dan wilayah Northwest Territories",
            "telepon": "(604) 682-8855",
            "fax": "(604) 662-8396",
            "email": "congen@indonesiavancouver.org",
            "website_detail": "https://kemlu.go.id/perwakilan/a3f390d88e4c41f2747bfa2f1b5f87db?type=perwakilan-detail"
        },
        "kolombia": {
            "name": "KBRI Bogota",
            "aliases": ["colombia"],
            "link": "https://kemlu.go.id/bogota",
            "address": "Calle 76 #10-02 Bogotá D.C.",
            "wilayah_akreditasi": "Merangkap Antigua dan Barbuda, Barbados, dan Federasi Saint Kitts dan Nevis",
            "telepon": "(+57-601) 755 03 34",
            "fax": "(+57-601) 755 03 35",
            "email": "bogota.kbri@kemlu.go.id",
            "website_detail": "https://kemlu.go.id/perwakilan/1f0e3dad99908345f7439f8ffabdffc4?type=perwakilan-detail"
        },
        "kuba": {
            "name": "KBRI Havana",
            "aliases": ["cuba"],
            "link": "https://kemlu.go.id/havana",
            "address": "5ta Avenida # 1607 Miramar, La Habana, Cuba",
            "wilayah_akreditasi": "Merangkap Persemakmuran Bahama, Republik Dominika, Republik Haiti dan Jamaika",
            "telepon": "(53) 7204-9963, 7204-9618, 7204-0046",
            "fax": "(53) 7204-9617",
            "email": "havana.kbri@kemlu.go.id",
            "website_detail": "https://kemlu.go.id/perwakilan/a1d0c6e83f027327d8461063f4ac58a6?type=perwakilan-detail"
        },
        "meksiko": {
            "name": "KBRI Mexico City",
            "aliases": ["mexico"],
            "link": "https://kemlu.go.id/mexicocity",
            "address": "Julio Verne No. 27, Colonia Polanco, Delegacion Miguel Hidalgo, Mexico City 11560, Mexico",
            "wilayah_akreditasi": "Meksiko",
            "telepon": "(+52-55) 5280 6363, 5282 1000, (HOTLINE) (+52) 5562 9855 06",
            "fax": "(+52-55) 5280-7062",
            "email": "mexico.kbri@kemlu.go.id",
            "website_detail": "https://kemlu.go.id/perwakilan/072b030ba126b2f4b2374f342be9ed44?type=perwakilan-detail"
        },
        "panama": {
            "name": "KBRI Panama City",
            "aliases": [],
            "link": "https://kemlu.go.id/panama",
            "address": "Casa No. 15, Av. Ricardo Arango y Calle 55 Este | Obarrio, Panama City",
            "wilayah_akreditasi": "Panama",
            "telepon": "(+507) 223 2100, Hotline: +507 6354-0958",
            "fax": None,
            "email": "panama.kbri@kemlu.go.id",
            "website_detail": "https://kemlu.go.id/perwakilan/14bfa6bb14875e45bba028a21ed38046?type=perwakilan-detail"
        },
        "peru": {
            "name": "KBRI Lima",
            "aliases": [],
            "link": "https://kemlu.go.id/lima",
            "address": "Calle Las Flores 334-336, San Isidro, Lima - Peru",
            "wilayah_akreditasi": "Merangkap Negara Plurinasional Bolivia",
            "telepon": "(511) 222-0308, 222-0309, 222-2822, Hotline: +51 913 210 991",
            "fax": None,
            "email": "lima.kbri@kemlu.go.id",
            "website_detail": "https://kemlu.go.id/perwakilan/d82c8d1619ad8176d665453cfb2e55f0?type=perwakilan-detail"
        },
        "suriname": {
            "name": "KBRI Paramaribo",
            "aliases": [],
            "link": "https://kemlu.go.id/paramaribo",
            "address": "Van Brussellaan #3, Uitvlugt, Paramaribo, Suriname",
            "wilayah_akreditasi": "Merangkap Republik Guyana",
            "telepon": "(597) 431-230, 431-171",
            "fax": "(597) 498-234",
            "email": "paramaribo.kbri@kemlu.go.id",
            "website_detail": "https://kemlu.go.id/perwakilan/7cbbc409ec990f19c78c75bd1e06f215?type=perwakilan-detail"
        },
        "venezuela": {
            "name": "KBRI Caracas",
            "aliases": [],
            "link": "https://kemlu.go.id/caracas",
            "address": "Avenida El Paseo,Urb. Prado del Este, Caracas, Municipio Baruta, Estado Miranda, 1080 Caracas, Venezuela",
            "wilayah_akreditasi": "Venezuela",
            "telepon": "+58 212 9751095, +58 412 2340100 (Hotline)",
            "fax": "58 212 9751075",
            "email": "caracas.kbri@kemlu.go.id",
            "website_detail": "https://kemlu.go.id/perwakilan/6ea9ab1baa0efb9e19094440c317e21b?type=perwakilan-detail"
        }
    },
    "Australia & Oseania": {
        "australia": {
            "name": "KBRI Canberra",
            "aliases": ["aussie"],
            "link": "https://kemlu.go.id/canberra",
            "address": "8 Darwin Avenue, Yarralumla Canberra, ACT 2600 Australia",
            "wilayah_akreditasi": "Merangkap Republik Vanuatu",
            "telepon": "+61262508600",
            "fax": "+61262733545, +61262736017",
            "email": "canberra.kbri@kemlu.go.id",
            "website_detail": "https://kemlu.go.id/perwakilan/02e74f10e0327ad868d138f2b4fdd6f0?type=perwakilan-detail"
        },
        "darwin": {
            "name": "KRI Darwin",
            "aliases": [],
            "link": "https://kemlu.go.id/darwin",
            "address": "20 Harry Chan Avenue - Darwin N.T. 0800",
            "wilayah_akreditasi": "Northern Territory of Australia",
            "telepon": "+61 (08) 8943 0200",
            "fax": "+61 (08) 8941 2709",
            "email": "darwin.kri@kemlu.go.id",
            "website_detail": "https://kemlu.go.id/perwakilan/02e74f10e0327ad868d138f2b4fdd6f0?type=perwakilan-detail"
        },
        "melbourne": {
            "name": "KJRI Melbourne",
            "aliases": [],
            "link": "https://kemlu.go.id/melbourne",
            "address": "72 Queens Road, Melbourne, VIC 3004 (Entrance From 72 Queens Lane)",
            "wilayah_akreditasi": "Negara Bagian Victoria, dan Tasmania",
            "telepon": "+61 3 9525 2755",
            "fax": None,
            "email": "melbourne.kjri@kemlu.go.id",
            "website_detail": "https://kemlu.go.id/perwakilan/02e74f10e0327ad868d138f2b4fdd6f0?type=perwakilan-detail"
        },
        "perth": {
            "name": "KJRI Perth",
            "aliases": [],
            "link": "https://kemlu.go.id/perth",
            "address": "134 Adelaide Terrace, East Perth, WA, 6004, Australia",
            "wilayah_akreditasi": "Australia Barat, Kepulauan Cocos, dan Pulau Christmas",
            "telepon": "(61-8)9221 5858",
            "fax": "(61-8)9221 5688",
            "email": "perth.kjri@kemlu.go.id",
            "website_detail": "https://kemlu.go.id/perwakilan/02e74f10e0327ad868d138f2b4fdd6f0?type=perwakilan-detail"
        },
        "sydney": {
            "name": "KJRI Sydney",
            "aliases": [],
            "link": "https://kemlu.go.id/sydney",
            "address": "236-238 Maroubra Road, Maroubra 2035",
            "wilayah_akreditasi": "Negara Bagian New South Wales, South Australia, dan Queensland",
            "telepon": "(02) 9314 0872/ 02 8347 6800 atau Hotline Pelindungan WNI +61 434544478",
            "fax": "+61 2 9349 6854",
            "email": "info.sydney@kemlu.go.id",
            "website_detail": "https://kemlu.go.id/perwakilan/02e74f10e0327ad868d138f2b4fdd6f0?type=perwakilan-detail"
        },
        "fiji": {
            "name": "KBRI Suva",
            "aliases": [],
            "link": "https://kemlu.go.id/suva",
            "address": "6th Floor Ra Marama Building, 91 Gordon Street, Suva, Fiji (P.O. BOX 878 Suva)",
            "wilayah_akreditasi": "Merangkap Republik Kiribati, Republik Nauru, dan Tuvalu",
            "telepon": "(679) 3316697",
            "fax": "(679) 3316696",
            "email": "suva.kbri@kemlu.go.id",
            "website_detail": "https://kemlu.go.id/perwakilan/c7e1249ffc03eb9ded908c236bd1996d?type=perwakilan-detail"
        },
        "new caledonia": {
            "name": "KJRI Noumea",
            "aliases": ["kaledonia baru"],
            "link": "https://kemlu.go.id/noumea",
            "address": "BP 26 98845 NOUMEA CEDEX New Caledonia",
            "wilayah_akreditasi": "Kaledonia Baru",
            "telepon": "(687) 23.28.81",
            "fax": "(687) 29 12 10",
            "email": "kjri.noumea@kemlu.go.id",
            "website_detail": "https://kemlu.go.id/perwakilan/fc490ca45c00b1249bbe3554a4fdf6fb?type=perwakilan-detail"
        },
        "papua nugini": {
            "name": "KBRI Port Moresby",
            "aliases": ["papua new guinea"],
            "link": "https://kemlu.go.id/portmoresby",
            "address": "Sir John Guise Drive, Lot 1 - 2, Section 410 Port Moresby, Papua New Guinea",
            "wilayah_akreditasi": "Merangkap Kepulauan Solomon",
            "telepon": "(+675) 325-3544, 7396 3011 (Consular Hotline)",
            "fax": "(675) 325-0265",
            "email": "portmoresby.kbri@kemlu.go.id",
            "website_detail": "https://kemlu.go.id/perwakilan/32bb90e8976aab5298d5da10fe66f21d?type=perwakilan-detail"
        },
        "vanimo": {
            "name": "KRI Vanimo",
            "aliases": [],
            "link": "https://kemlu.go.id/vanimo",
            "address": "Vanimo, Sandaun Province, Papua New Guinea (P.O.BOX 39 VANIMO)",
            "wilayah_akreditasi": "Provinsi Sandaun, dan Western",
            "telepon": "(675) 857-1371, 857-1372",
            "fax": "(675) 857-1373",
            "email": "vanimo.kri@kemlu.go.id",
            "website_detail": "https://kemlu.go.id/perwakilan/32bb90e8976aab5298d5da10fe66f21d?type=perwakilan-detail"
        },
        "selandia baru": {
            "name": "KBRI Wellington",
            "aliases": ["new zealand", "nz"],
            "link": "https://kemlu.go.id/wellington",
            "address": "70 Glen Road, Kelburn Wellington, New Zealand",
            "wilayah_akreditasi": "Merangkap Samoa, Kerajaan Tonga, Kepulauan Cook dan Niue",
            "telepon": "64-4-4758 699",
            "fax": "64-4-4759 374",
            "email": "wellington.kbri@kemlu.go.id",
            "website_detail": "https://kemlu.go.id/perwakilan/26657d5ff9020d2abefe558796b99584?type=perwakilan-detail"
        }
    }
}