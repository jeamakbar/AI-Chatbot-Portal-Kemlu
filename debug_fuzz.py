from thefuzz import fuzz, process

# Kueri dan pilihan yang menyebabkan masalah
query = "neverland"
choices = [
    'netherlands', 
    'switzerland', 
    'thailand', 
    'finland', 
    'new zealand'
]
min_score = 80

print(f"Mencari '{query}' dalam daftar...")
print("-" * 30)

# 1. Periksa skor mentah
raw_score = fuzz.WRatio(query, 'netherlands')
print(f"Skor mentah WRatio antara '{query}' dan 'netherlands' adalah: {raw_score}")

# 2. Uji fungsi extractOne dengan score_cutoff
result = process.extractOne(
    query,
    choices,
    scorer=fuzz.WRatio,
    score_cutoff=min_score
)

print(f"Hasil dari process.extractOne dengan score_cutoff={min_score} adalah: {result}")
print("-" * 30)

if result is None:
    print("✅ HASIL BENAR: Tidak ada kecocokan yang ditemukan di atas ambang batas.")
else:
    print("❌ HASIL SALAH: Seharusnya mengembalikan None, tetapi menemukan kecocokan.")