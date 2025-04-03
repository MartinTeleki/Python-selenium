import json
import os
from datetime import datetime

# Mapa klíčů z textu na JSON klíče
key_map = {
    "Rok registrace": "rok_registrace",
    "Značka": "znacka",
    "Model": "model",
    "VIN": "vin",
    "Jméno": "jmeno",
    "Příjmení": "prijmeni",
    "Email": "email",
    "Najeto km": "najeto_km"
}

# Přečti soubor
with open("text_form.txt", "r", encoding="utf-8") as file:
    lines = file.read().strip().split("\n")

entries = []
entry = {}

for line in lines:
    if not line.strip():  # prázdný řádek = konec jednoho záznamu
        if entry:
            entries.append({
                "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "url": "https://cloudalm.cz/formular/",
                "data": entry,
                "error": None,
                "message": None
            })
            entry = {}
    else:
        if ":" in line:
            key, value = line.split(":", 1)
            key = key.strip()
            value = value.strip()
            if key in key_map:
                entry[key_map[key]] = value

# Přidej poslední záznam, pokud není zakončen prázdným řádkem
if entry:
    entries.append({
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "url": "https://cloudalm.cz/formular/",
        "data": entry,
        "error": None,
        "message": None
    })

# Zajisti existenci složky "json"
output_dir = "json"
os.makedirs(output_dir, exist_ok=True)

# Dynamické pojmenování souboru
base_filename = os.path.join(output_dir, "form_data_result")
filename = f"{base_filename}.json"
i = 1
while os.path.exists(filename):
    filename = f"{base_filename}_{i}.json"
    i += 1

# Uložení výstupu
with open(filename, "w", encoding="utf-8") as f:
    json.dump(entries, f, ensure_ascii=False, indent=4)

# Výpis počtu záznamů
print(f"✅ Hotovo. Uloženo {len(entries)} záznamů do souboru: {filename}")
