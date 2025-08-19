

import os
import requests
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import time

BASE_URL = "https://www.perfumesdeoriente.com.ar/perfumes/?mpage=17"
IMG_DIR = "imagenes_productos"
os.makedirs(IMG_DIR, exist_ok=True)

# Configuración Selenium headless
chrome_options = Options()
chrome_options.add_argument('--headless')
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--disable-dev-shm-usage')
driver = webdriver.Chrome(options=chrome_options)

# Paso 1: Obtener links de productos desde la grilla
driver.get(BASE_URL)
time.sleep(2)
product_links = set()
elements = driver.find_elements(By.CSS_SELECTOR, "a[href*='/productos/']")
for el in elements:
    href = el.get_attribute('href')
    if href and '/productos/' in href:
        product_links.add(href)



import re
for link in product_links:
    print(f"Procesando: {link}")
    driver.get(link)
    time.sleep(2)
    # Extraer nombre del producto de la URL
    prod_name = re.sub(r"[^a-zA-Z0-9_-]", "", link.split("/")[-2])
    # Buscar enlaces <a> con href de imagen grande del slider
    a_tags = driver.find_elements(By.CSS_SELECTOR, "a[href]")
    img_urls = []
    for a in a_tags:
        href = a.get_attribute('href')
        if href and "/products/" in href and href.endswith("-1024-1024.webp"):
            # Normalizar URL si empieza con //
            if href.startswith("//"):
                href = "https:" + href
            img_urls.append(href)
    if not img_urls:
        print(f"No se encontraron imágenes grandes del slider para {prod_name}")
    for idx, src in enumerate(img_urls[:4]):
        nombre = f"{prod_name}_{idx+1}.webp"
        ruta = os.path.join(IMG_DIR, nombre)
        try:
            r = requests.get(src)
            with open(ruta, 'wb') as f:
                f.write(r.content)
            print(f"Descargada: {ruta}")
        except Exception as e:
            print(f"Error descargando {src}: {e}")
driver.quit()
print("Scraping finalizado.")
