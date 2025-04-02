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

# Spuštění WebDriveru
driver = webdriver.Edge()

for index, entry in enumerate(test_data):
    driver.get("https://cloudalm.cz/formular")

    # Výsledná struktura
    result = {
        "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
        "url": driver.current_url,
        "data": entry["data"],
        "error": None,
        "message": None
    }

    try:
        # Počkej na načtení formuláře
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.NAME, "wpforms[fields][1]")))
        time.sleep(2)

        # Validace vstupních dat
        error_message = test_form_data(entry)
        if error_message:
            raise ValueError(error_message)

        # Vyplnění formuláře
        driver.find_element(By.NAME, "wpforms[fields][1]").send_keys(result["data"]["rok_registrace"])
        driver.find_element(By.NAME, "wpforms[fields][2]").send_keys(result["data"]["znacka"])
        driver.find_element(By.NAME, "wpforms[fields][3]").send_keys(result["data"]["model"])
        driver.find_element(By.NAME, "wpforms[fields][4]").send_keys(result["data"]["vin"])
        driver.find_element(By.NAME, "wpforms[fields][8][first]").send_keys(result["data"]["jmeno"])
        driver.find_element(By.NAME, "wpforms[fields][8][last]").send_keys(result["data"]["prijmeni"])
        driver.find_element(By.NAME, "wpforms[fields][7]").send_keys(result["data"]["email"])
        driver.find_element(By.NAME, "wpforms[fields][5]").send_keys(result["data"]["najeto_km"])
        driver.find_element(By.NAME, "wpforms[fields][6]").send_keys(result["data"]["najeto_km"])

        # Najdi tlačítko a odešli
        submit_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.NAME, "wpforms[submit]"))
        )
        submit_button.click()

        # Počkej a zkontroluj, jestli web nevykazuje chybu (např. neplatný e-mail)
        time.sleep(5)
        try:
            error_element = driver.find_element(By.CLASS_NAME, "wpforms-error")
            result["error"] = f"Chyba z webu: {error_element.text}"
            result["message"] = "Formulář Nebyl přijat – webová validace selhala."
        except:
            result["message"] = "Formulář odeslán úspěšně."

    except Exception as e:
        result["error"] = str(e)
        result["message"] = "Chyba při zpracování záznamu."

        print(f"‼️ Chyba v záznamu {index + 1}: {e}")

    # Ulož výsledek do samostatného JSON souboru
    json_filename = f"C:\\Users\\teleki\\Desktop\\Hackathon2025\\json\\form_data_{index + 1}.json"
    with open(json_filename, "w", encoding="utf-8") as file:
        json.dump(result, file, ensure_ascii=False, indent=4)
        
    # Ulož JSON pouze pokud je chyba
    if result["error"]:
        json_filename = f"C:\\Users\\teleki\\Desktop\\Hackathon2025\\json\\form_data_{index + 1}_ERROR.json"
        with open(json_filename, "w", encoding="utf-8") as file:
            json.dump(result, file, ensure_ascii=False, indent=4)

    print(f"✅ Záznam {index + 1} zpracován.")
    print(json.dumps(result, ensure_ascii=False, indent=4))
 

# Zavření prohlížeče
driver.quit()
