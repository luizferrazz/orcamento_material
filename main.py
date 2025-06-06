from time import sleep
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.select import Select
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
import pandas as pd

def configurar_driver():
    try:
        options = Options()
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--start-maximized")
        options.add_experimental_option("prefs", {
            "profile.default_content_setting_values.notifications": 1,
            "profile.default_content_setting_values.geolocation": 1,
            "download.prompt_for_download": False
        })
        options.add_argument("--use-fake-ui-for-media-stream")
        options.add_argument("--use-fake-device-for-media-stream")
        options.add_argument("--enable-cookies")
        
        service = Service(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=options)
        return driver
    except Exception as e:
        print(f"Erro ao configurar o driver: {e}")
        return None
    
def acessar_dental_cremer(driver):
    try:
        driver.get("https://www.dentalcremer.com.br/")

        sleep(3)

        try:

            btn_aceitar_cookies = WebDriverWait(driver, 20).until(
                EC.presence_of_element_located((By.XPATH, '//*[@id="onetrust-accept-btn-handler"]'))
            )
            btn_aceitar_cookies.click()
        
        except Exception as e:
            pass

        return True
    except Exception as e:
        print(f"Erro ao acessar dental: {str(e)}")

def pesquisar_itens(driver, lista_itens):
    try:
        menores_precos = []
        for item in lista_itens:

            input_busca = WebDriverWait(driver, 20).until(
                EC.presence_of_element_located((By.XPATH, '//*[@id="search"]'))
            )  
            input_busca.clear()
            input_busca.send_keys(item)
            input_busca.send_keys(Keys.ENTER)

            select_numero_itens = WebDriverWait(driver, 20).until(
                EC.presence_of_element_located((By.XPATH, '//*[@id="limiter"]'))
            )
            select = Select(select_numero_itens)
            options = select.options
            select.select_by_index(len(options) - 1)

            menores_precos = orcar_item(driver, menores_precos)

        return True, menores_precos

    except Exception as e:
        print(f"Erro ao pesquisar itens: {str(e)}")
        return False, menores_precos

def orcar_item(driver, menores_precos):
    try:
        lista_ordenada = WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.XPATH, '//*[@id="linx-search"]/div[2]/div[3]/div[1]/div[1]/div[3]/ol'))
        )
        WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located((By.CLASS_NAME, "product-item"))
        )
        items = lista_ordenada.find_elements(By.CLASS_NAME, "product-item")
        menor_preco = float('inf')
        item_menor_preco = None

        for item in items:
            try:
                preco_texto = item.find_element(By.CLASS_NAME, "product-item-price").text
                preco = float(preco_texto.replace('R$', '').replace('.', '').replace(',', '.').strip())
                
                if preco < menor_preco:
                    menor_preco = preco
                    item_menor_preco = item
            except:
                continue

        if item_menor_preco:
            print(f"Menor preço encontrado no item: R$ {menor_preco:.2f}")
            menores_precos.append(menor_preco)
            print(f"O item de menor preco eh: {menores_precos}")

        return menores_precos
    
    except Exception as e:
        print(f"Erro ao orcar item: {str(e)}")

def main():

    driver = configurar_driver()

    if not driver:
        return

    if not acessar_dental_cremer(driver):
        return
    
    lista_itens = ["sugador descartável", "luva p", "gaze estéril"]
    #print("Colunas do arquivo:", lista_itens.columns)

    status, menores_precos =  pesquisar_itens(driver, lista_itens)

    print(menores_precos)

    if not status:
        return


if __name__ == "__main__":
    main()