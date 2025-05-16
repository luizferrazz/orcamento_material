import os
from time import sleep
import random
import time
import pyotp
from dotenv import load_dotenv
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.select import Select
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from datetime import datetime
from docx import Document
from docx2pdf import convert
import logging
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
import pyautogui

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
        sleep(5)
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
        for item in lista_itens:

            input_busca = WebDriverWait(driver, 20).until(
                EC.presence_of_element_located((By.XPATH, '//*[@id="search"]'))
            )  
            input_busca.clear()
            input_busca.send_keys(item)
            input_busca.send_keys(Keys.ENTER)

        return True

    except Exception as e:
        print(f"Erro ao pesquisar itens: {str(e)}")

def main():

    driver = configurar_driver()

    if not driver:
        return

    if not acessar_dental_cremer(driver):
        return
    
    lista_itens = ["gaze", "luva p", "lamina de bisturi 15"]

    if not pesquisar_itens(driver, lista_itens):
        return


if __name__ == "__main__":
    main()