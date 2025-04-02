from selenium import webdriver # WebDriver pro ovládání prohlížeče
from selenium.webdriver.common.by import By  # Pro vyhledávání prvků na stránce
from selenium.webdriver.common.keys import Keys # Pro simulaci klávesnice (např. ENTER)
import time  # Modul pro zpoždění mezi akcemi

driver = webdriver.Edge() # Spuštění Edge WebDriveru
#driver.get("https://www.selenium.dev/selenium/web/web-form.html")
driver.get("http://cloudalm.cz") # Otevření webové stránky
title = driver.title # Získání titulku stránky
print(title)

links = driver.find_elements(By.TAG_NAME, "a")
for link in links:
    print(link.text, "->", link.get_attribute("href"))

heading = driver.find_element(By.TAG_NAME, "h1")
print("Hlavní nadpis:", heading.text)

try:
    heading_h2 = driver.find_element(By.TAG_NAME, "h2").text
    print("Hlavní nadpis (h2):", heading_h2)
except:
    print("H2 nadpis nenalezen.")

#input_field = driver.find_element(By.NAME, "some-input-name")
#input_field.send_keys("Testovací zpráva")



# Vyhledání tlačítka pomocí CSS selektoru a kliknutí
try:
    button = driver.find_element(By.CSS_SELECTOR, "button[type='submit']")
    button.click()
    print("Tlačítko bylo kliknuto.")
except:
    print("Tlačítko nenalezeno.")

    # Otevře stránku s formulářem
driver.get("https://cloudalm.cz/formular/")  # Změň na správnou URL

    # Počkáme chvíli, aby se stránka načetla
time.sleep(5)

    # Použití Keys k odeslání formuláře
driver.find_element(By.NAME, "rok_registrace").send_keys("2020")
driver.find_element(By.NAME, "vyrobce").send_keys("Škoda")
driver.find_element(By.NAME, "model").send_keys("Kodiaq")
driver.find_element(By.NAME, "vin").send_keys("WVWZZZ3CZ8E123456")
driver.find_element(By.NAME, "jmeno").send_keys("Martin")
driver.find_element(By.NAME, "prijmeni").send_keys("Novák")
driver.find_element(By.NAME, "email").send_keys("martin.novak@example.com")
driver.find_element(By.NAME, "pocet_km").send_keys("65000")
driver.find_element(By.NAME, "rocni_najezd").send_keys("15000")

driver.quit()
print("Driver ukončen.")
