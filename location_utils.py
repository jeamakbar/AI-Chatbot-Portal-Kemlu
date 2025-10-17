from thefuzz import fuzz, process
from constants import PERWAKILAN_DATA

# --- PEMBUATAN PEMETAAN DINAMIS ---
CITY_TO_COUNTRY_MAPPING = {}
ALL_LOCATIONS = []

def build_location_data():
    """Membangun pemetaan dan daftar datar lokasi untuk pencocokan fuzzy."""
    if ALL_LOCATIONS:
        return

    for continent, countries in PERWAKILAN_DATA.items():
        CITY_TO_COUNTRY_MAPPING[continent] = {}
        for country_key, details in countries.items():
            ALL_LOCATIONS.append(country_key.lower())
            if details.get("aliases"):
                ALL_LOCATIONS.extend([alias.lower() for alias in details["aliases"]])

            name_parts = details['name'].split(' ')
            if len(name_parts) > 1:
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
    return list(set(cities))

# FINAL FIX: Increased the min_score threshold to 85 to reject the unwanted match that scores 80.
def find_location_info(text_query: str, min_score=85) -> tuple[dict | None, int]:
    """
    Menemukan informasi kantor perwakilan menggunakan pencocokan fuzzy.
    """
    location_query = text_query.lower().strip().rstrip('?.,!')

    result = process.extractOne(
        location_query, 
        ALL_LOCATIONS, 
        scorer=fuzz.WRatio, 
        score_cutoff=min_score
    )
    
    if result is None:
        return None, 0
        
    best_match, score = result

    for continent_data in PERWAKILAN_DATA.values():
        for country_key, data in continent_data.items():
            match_candidates = [country_key.lower()] + [alias.lower() for alias in data.get("aliases", [])]
            name_parts = data['name'].split(' ')
            if len(name_parts) > 1:
                city_name = ' '.join(name_parts[1:]).lower()
                if city_name:
                    match_candidates.append(city_name)
            
            if best_match.lower() in match_candidates:
                return data, score
    
    return None, 0