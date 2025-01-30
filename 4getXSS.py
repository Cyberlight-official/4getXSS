import os
import time
import logging
import requests
import threading
import json
from urllib.parse import urlparse, parse_qs, urlencode, urlunparse
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.alert import Alert
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from colorama import Fore
from queue import Queue


os.system('clear')

# 4getXSS - Advanced XSS Scanner
print('''\033[0;31m
_________________________________________
|  _  _              _  __  ____  __    |
| | || |   __ _  ___| |_\ \/ / _\/ _\   |
| | || |_ / _` |/ _ \ __|\  /\ \ \ \    |
| |__   _| (_| |  __/ |_ /  \_\ \_\ \   |
|    |_|  \__, |\___|\__/_/\_\__/\__/   |
|         |___/                         |
|_______________________________________|
\033[0;36m Author: Rezuan Sowad (4get)
''')

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

driver_pool = Queue()
driver_lock = threading.Lock()

def initialize_driver():
    chrome_options = Options()
    chrome_options.add_argument("--headless")  # Run in background
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=chrome_options)
    return driver

def load_payloads(payload_file):
 
    try:
        with open(payload_file, 'r') as f:
            return [line.strip() for line in f if line.strip()]
    except Exception as e:
        print(Fore.RED + f"Error loading payloads: {e}")
        return []

def generate_payload_urls(base_url, payload):
   
    url_parts = urlparse(base_url)
    query_params = parse_qs(url_parts.query, keep_blank_values=True)
    modified_urls = []
    
    for param in query_params:
        new_params = query_params.copy()
        new_params[param] = [payload]
        new_query_string = urlencode(new_params, doseq=True)
        new_url = urlunparse((url_parts.scheme, url_parts.netloc, url_parts.path, '', new_query_string, ''))
        modified_urls.append(new_url)
    
    return modified_urls

def check_for_xss(url, payload, timeout, scan_results):
  
    driver = get_driver_from_pool()
    try:
        urls_to_check = generate_payload_urls(url, payload)
        for test_url in urls_to_check:
            try:
                driver.get(test_url)
                WebDriverWait(driver, timeout).until(EC.alert_is_present())
                alert = Alert(driver)
                alert_text = alert.text
                alert.accept()
                
                if alert_text:
                    print(Fore.GREEN + f"[✓] Vulnerable URL: {test_url} - Alert Text: {alert_text}")
                    result = {
                        'url': test_url,
                        'payload': payload,
                        'alert_text': alert_text
                    }
                    with driver_lock:
                        scan_results.append(result)
                else:
                    print(Fore.RED + f"[✗] Not Vulnerable: {test_url}")
            except Exception as e:
                print(Fore.YELLOW + f"[!] Error processing {test_url}: {e}")
    finally:
        return_driver_to_pool(driver)

def get_driver_from_pool():
   
    try:
        return driver_pool.get_nowait()
    except:
        with driver_lock:
            return initialize_driver()

def return_driver_to_pool(driver):
   
    driver_pool.put(driver)

def run_xss_scan(urls, payload_file, timeout, scan_results):
  
    payloads = load_payloads(payload_file)
    for url in urls:
        for payload in payloads:
            check_for_xss(url, payload, timeout, scan_results)

def print_scan_summary(scan_results, start_time):
 
    total_time = time.time() - start_time
    print(Fore.YELLOW + "\n[+] Scan Complete!")
    print(f"Total URLs scanned: {len(scan_results)}")
    print(f"Total scan time: {total_time:.2f} seconds")

def save_report_to_json(scan_results, filename):
   
    try:
        with open(filename, 'w') as file:
            json.dump(scan_results, file, indent=4)
        print(Fore.GREEN + f"[+] JSON Report saved as {filename}")
    except Exception as e:
        print(Fore.RED + f"Error saving JSON report: {e}")

def clear_screen():
  
    os.system('cls' if os.name == 'nt' else 'clear')

def run():
  
    urls_input = input(Fore.CYAN + "Enter target URLs (comma-separated): ").strip()
    urls = [url.strip() for url in urls_input.split(',')]
    payload_file = input(Fore.CYAN + "Enter the path to the XSS payload file: ").strip()
    timeout = int(input(Fore.CYAN + "Enter the timeout for detecting alerts (seconds): ").strip())
    
    scan_results = []
    
    print(Fore.YELLOW + "\n[+] Starting scan...")
    start_time = time.time()
    
    run_xss_scan(urls, payload_file, timeout, scan_results)
    
    print_scan_summary(scan_results, start_time)
    
    if scan_results:
        save_report = input(Fore.CYAN + "[?] Would you like to generate a JSON report? (y/n): ").strip().lower()
        if save_report == 'y':
            report_filename = input(Fore.CYAN + "[?] Enter the filename for the JSON report: ").strip() or "4getXSS_scan_report.json"
            save_report_to_json(scan_results, report_filename)

if __name__ == "__main__":
    run()
