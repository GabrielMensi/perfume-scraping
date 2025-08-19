

import os
import sys

print("=" * 50)
print("🚀 SCRAPER DE PERFUMES - INICIANDO")
print("=" * 50)

# Verificar versión de Python
print(f"🐍 Python {sys.version}")

try:
    print("📦 Importando librerías...")
    import requests
    print("  ✓ requests")
    
    from selenium import webdriver
    from selenium.webdriver.chrome.options import Options
    from selenium.webdriver.chrome.service import Service
    print("  ✓ selenium")
    
    from webdriver_manager.chrome import ChromeDriverManager
    print("  ✓ webdriver-manager")
    
    from selenium.webdriver.common.by import By
    print("  ✓ selenium.webdriver.common.by")
    
    import time
    print("  ✓ time")
    
    print("✅ Todas las librerías importadas correctamente")
    
except ImportError as e:
    print(f"❌ Error importando librerías: {e}")
    print("\n💡 Solución:")
    print("Ejecuta: pip install requests beautifulsoup4 selenium webdriver-manager")
    input("\nPresiona Enter para salir...")
    exit(1)
except Exception as e:
    print(f"❌ Error inesperado: {e}")
    input("\nPresiona Enter para salir...")
    exit(1)

BASE_URL = "https://www.perfumesdeoriente.com.ar/perfumes/?mpage=17"
IMG_DIR = "imagenes_productos"

try:
    os.makedirs(IMG_DIR, exist_ok=True)
    print(f"� Carpeta de imágenes: {os.path.abspath(IMG_DIR)}")
except Exception as e:
    print(f"❌ Error creando carpeta: {e}")
    input("Presiona Enter para salir...")
    exit(1)

try:
    # Configuración Selenium headless
    print("⚙️ Configurando navegador...")
    chrome_options = Options()
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')
    chrome_options.add_argument('--disable-gpu')
    chrome_options.add_argument('--window-size=1920,1080')

    # Usar webdriver-manager para descargar automáticamente ChromeDriver
    print("🔧 Descargando ChromeDriver...")
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=chrome_options)
    print("✅ Navegador configurado correctamente")

except Exception as e:
    print(f"❌ Error configurando el navegador: {e}")
    print("💡 Asegúrate de que Google Chrome esté instalado")
    input("Presiona Enter para salir...")
    exit(1)

# Paso 1: Obtener links de productos desde la grilla
try:
    print("🌐 Conectando a la página web...")
    driver.get(BASE_URL)
    time.sleep(2)
    print("✅ Página cargada correctamente")
    
    print("🔍 Buscando productos...")
    product_links = set()
    elements = driver.find_elements(By.CSS_SELECTOR, "a[href*='/productos/']")
    for el in elements:
        href = el.get_attribute('href')
        if href and '/productos/' in href:
            product_links.add(href)
    
    print(f"📦 Encontrados {len(product_links)} productos")
    
    if len(product_links) == 0:
        print("⚠️ No se encontraron productos. Verifica la URL y tu conexión.")
        driver.quit()
        input("Presiona Enter para salir...")
        exit(1)
        
except Exception as e:
    print(f"❌ Error accediendo a la página: {e}")
    print("💡 Verifica tu conexión a internet")
    driver.quit()
    input("Presiona Enter para salir...")
    exit(1)



import re

print("🖼️ Comenzando descarga de imágenes...")
total_productos = len(product_links)
contador = 0

for link in product_links:
    contador += 1
    try:
        print(f"[{contador}/{total_productos}] Procesando producto...")
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
            print(f"⚠️ No se encontraron imágenes para {prod_name}")
            continue
            
        # Descargar hasta 4 imágenes por producto
        for idx, src in enumerate(img_urls[:4]):
            nombre = f"{prod_name}_{idx+1}.webp"
            ruta = os.path.join(IMG_DIR, nombre)
            try:
                r = requests.get(src, timeout=10)
                r.raise_for_status()
                with open(ruta, 'wb') as f:
                    f.write(r.content)
                print(f"  ✅ Descargada: {nombre}")
            except Exception as e:
                print(f"  ❌ Error descargando {nombre}: {e}")
                
    except Exception as e:
        print(f"❌ Error procesando producto {contador}: {e}")
        continue

driver.quit()
print(f"🎉 Scraping finalizado. Se procesaron {contador} productos.")
print(f"📁 Revisa la carpeta '{IMG_DIR}' para ver las imágenes descargadas.")
input("Presiona Enter para salir...")
