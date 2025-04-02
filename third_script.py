import json
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Načtení souboru s testovacími daty
with open('C:\\Users\\teleki\\Desktop\\Hackathon2025\\json\\form_data_result.json', 'r', encoding='utf-8') as file:
    test_data = json.load(file)

# Testovací funkce pro ověření dat
def test_form_data(entry):
    try:
        assert 'timestamp' in entry, "Chybí timestamp"
        assert 'url' in entry, "Chybí URL"
        assert 'data' in entry, "Chybí data"
        assert 'error' in entry, "Chybí error"
        assert 'message' in entry, "Chybí message"
        assert 'rok_registrace' in entry['data'], "Chybí rok registrace"
        assert 'znacka' in entry['data'], "Chybí značka"
        assert 'model' in entry['data'], "Chybí model"
        assert 'vin' in entry['data'], "Chybí VIN"
        assert 'jmeno' in entry['data'], "Chybí jméno"
        assert 'prijmeni' in entry['data'], "Chybí příjmení"
        assert 'email' in entry['data'], "Chybí email"
        assert 'najeto_km' in entry['data'], "Chybí najeté kilometry"
        return None  # žádná chyba
    except AssertionError as e:
        return str(e)


# Spuštění WebDriveru a otevření stránky
driver = webdriver.Edge()
driver.get("https://cloudalm.cz/formular")

# Počkejte, dokud nebude stránka načtena
WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.NAME, "wpforms[fields][1]")))

# Iterace přes všechna data v JSON
for index, entry in enumerate(test_data):
    # Před každou iterací znovu načíst stránku nebo resetovat formulář, aby byly připravené pole pro nový záznam
    driver.get("https://cloudalm.cz/formular")  # Znovu načíst stránku

    # Počkejte, dokud bude stránka připravena pro vyplnění
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.NAME, "wpforms[fields][1]")))

    time.sleep(2)

    result = {
        "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
        "url": driver.current_url,
        "data": entry["data"],  # Přiřazení hodnot do result["data"]
        "error": None,
        "message": None
    }

    error_message = test_form_data(entry)  # ← Tohle volá validaci

    if error_message:
        print(f"‼️ Chyba v záznamu {index + 1}: {error_message}")
    else:
        # Vyplnění a odeslání formuláře jen když je validní
        driver.find_element(By.NAME, "wpforms[fields][1]").send_keys(result["data"]["rok_registrace"])
        driver.find_element(By.NAME, "wpforms[fields][2]").send_keys(result["data"]["znacka"])
        driver.find_element(By.NAME, "wpforms[fields][3]").send_keys(result["data"]["model"])
        driver.find_element(By.NAME, "wpforms[fields][4]").send_keys(result["data"]["vin"])
        driver.find_element(By.NAME, "wpforms[fields][8][first]").send_keys(result["data"]["jmeno"])
        driver.find_element(By.NAME, "wpforms[fields][8][last]").send_keys(result["data"]["prijmeni"])
        driver.find_element(By.NAME, "wpforms[fields][7]").send_keys(result["data"]["email"])
        driver.find_element(By.NAME, "wpforms[fields][5]").send_keys(result["data"]["najeto_km"])
        driver.find_element(By.NAME, "wpforms[fields][6]").send_keys(result["data"]["najeto_km"])
        driver.find_element(By.NAME, "wpforms[submit]").submit()
        time.sleep(5)
    # Odeslání formuláře
    submit_button = driver.find_element(By.NAME, "wpforms[submit]")
    submit_button.submit()

    # Počkejte na zpracování formuláře, než uložíme výsledky
    time.sleep(5)

    # Uložení do JSON souboru pro každý záznam
    json_filename = f"C:\\Users\\teleki\\Desktop\\Hackathon2025\\json\\form_data_{index + 1}.json"  # Uložíme každý záznam s unikátním názvem
    with open(json_filename, "w", encoding="utf-8") as file:
        json.dump(result, file, ensure_ascii=False, indent=4)

    # Výpis do terminálu
    print(f"Testování pro záznam {index + 1} prošlo úspěšně!")
    print(json.dumps(result, ensure_ascii=False, indent=4))

# Zavření prohlížeče
driver.quit()

# Volání funkce pro testování dat
test_form_data(test_data)
