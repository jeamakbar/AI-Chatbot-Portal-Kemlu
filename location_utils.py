from thefuzz import fuzz, process
from constants import PERWAKILAN_DATA

# --- PEMBUATAN PEMETAAN DINAMIS ---
CITY_TO_COUNTRY_MAPPING = {}
ALL_LOCATIONS = []

def build_location_data():
    """Membangun pemetaan dan daftar datar lokasi untuk pencocokan fuzzy."""
    if ALL_LOCATIONS: # Hanya membangun data sekali saja
        return

    for continent, countries in PERWAKILAN_DATA.items():
        CITY_TO_COUNTRY_MAPPING[continent] = {}
        for country_key, details in countries.items():
            # Menambahkan negara dan aliasnya ke daftar
            ALL_LOCATIONS.append(country_key.lower())
            if details.get("aliases"):
                ALL_LOCATIONS.extend([alias.lower() for alias in details["aliases"]])

            # Ekstrak nama kota dan petakan
            name_parts = details['name'].split(' ')
            if len(name_parts) > 1:
                # Mengambil semua kata setelah kata pertama sebagai nama kota
                city_name = ' '.join(name_parts[1:]).lower()
                CITY_TO_COUNTRY_MAPPING[continent][city_name] = country_key
                if city_name not in ALL_LOCATIONS:
                    ALL_LOCATIONS.append(city_name)

# --- INISIALISASI DATA LOKASI SAAT STARTUP ---
build_location_data()

def get_all_cities():
    """Mengambil semua nama kota dari data perwakilan."""
    cities = []
    for continent_cities in CITY_TO_COUNTRY_MAPPING.values():
        cities.extend(continent_cities.keys())
    return list(set(cities)) # Mengembalikan nilai unik

def find_location_info(text_query: str, min_score=80) -> tuple[dict | None, int]:
    """
    Menemukan informasi kantor perwakilan menggunakan pencocokan fuzzy pada nama, kota, dan alias.
    Mengembalikan tuple (info_lokasi, skor).
    """
    location_query = text_query.lower().strip().rstrip('?.,!')

    # Menggunakan pencocokan fuzzy untuk menemukan kecocokan terbaik dari semua nama yang mungkin
    best_match, score = process.extractOne(location_query, ALL_LOCATIONS, scorer=fuzz.ratio)

    if score < min_score:
        return None, 0

    # Setelah mendapatkan kecocokan terbaik, temukan objek data lengkap yang sesuai
    for continent_data in PERWAKILAN_DATA.values():
        for country_key, data in continent_data.items():
            # Periksa apakah kecocokan terbaik adalah kunci negara, alias, atau nama kota
            match_candidates = [country_key.lower()] + [alias.lower() for alias in data.get("aliases", [])]
            city_name = ' '.join(data['name'].split(' ')[1:]).lower()
            if city_name:
                match_candidates.append(city_name)

            if best_match.lower() in match_candidates:
                return data, score

    return None, 0