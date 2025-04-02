import json
from selenium import webdriver # WebDriver pro ovládání prohlížeče
from selenium.webdriver.common.by import By  # Pro vyhledávání prvků na stránce
from selenium.webdriver.common.keys import Keys # Pro simulaci klávesnice (např. ENTER)
import time  # Modul pro zpoždění mezi akcemi

driver = webdriver.Edge() # Spuštění Edge WebDriveru
driver.get("https://cloudalm.cz/formular")  # Změň na správnou URL
time.sleep(5)

# Struktura pro ukládání výsledků
result = {
    "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
    "url": driver.current_url,
    "data": {},
    "error": None,
    "message": None
}

driver.find_element(By.NAME, "wpforms[fields][1]").send_keys("2020") # 2020
driver.find_element(By.NAME, "wpforms[fields][2]").send_keys("Škoda ") ## Škoda    
driver.find_element(By.NAME, "wpforms[fields][3]").send_keys("Kodiaq") # Kodiaq
driver.find_element(By.NAME, "wpforms[fields][4]").send_keys("1HGBH41JXMN109123") # 1HGBH41JXMN109123
driver.find_element(By.NAME, "wpforms[fields][8][first]").send_keys("Martin ") # Martin 
driver.find_element(By.NAME, "wpforms[fields][8][last]").send_keys("Teleki") # Teleki
driver.find_element(By.NAME, "wpforms[fields][7]").send_keys("martinteleki@seznam.cz") # martinteleki@seznam.cz
driver.find_element(By.NAME, "wpforms[fields][5]").send_keys("10 000") # 10 000
driver.find_element(By.NAME, "wpforms[fields][6]").send_keys("25 000") # 25 000
#driver.find_element(By.NAME, "wpforms[fields][9]").send_keys("2020") # Odeslání formuláře

    # Uložení dat, která jsme vyplnili

result["data"] = {
        "rok_registrace": "2020",
        "znacka": "Škoda",
        "model": "Kodiaq",
        "vin": "1HGBH41JXMN109123",
        "jmeno": "Martin",
        "prijmeni": "Teleki",
        "email": "martinteleki@seznam.cz",
        "najeto_km": "10 000"
    }

time.sleep(5)

# Odeslání formuláře pomocí submit
submit_button = driver.find_element(By.NAME, "wpforms[submit]")
submit_button.submit()

#driver.find_element(By.NAME, "wpforms[submit]").click()
time.sleep(5)


    # Získání zprávy po odeslání


# Uložení do JSON souboru
json_filename = "C:\\Users\\teleki\\Desktop\\Hackathon2025\\json\\form_data.json"

with open(json_filename, "w", encoding="utf-8") as file:
    json.dump(result, file, ensure_ascii=False, indent=4)

    # Výpis do terminálu
print(json.dumps(result, ensure_ascii=False, indent=4))













