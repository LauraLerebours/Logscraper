from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from twilio.rest import Client
import time

# ======== CONFIGURATION ========
MAZEVO_URL = "https://events.mit.edu/mazevo"  # Update if needed
# LOGIN_URL = "https://events.mit.edu/mazevo/login"  # Confirm login URL
LOGIN_URL = "https://mymazevo.com/login"
USERNAME = "your_mazevo_username"
PASSWORD = "your_mazevo_password"

TWILIO_SID = "your_twilio_sid"
TWILIO_AUTH = "your_twilio_auth_token"
FROM_NUM = "your_twilio_number"
TO_NUM = "your_boss_number"

CHROMEDRIVER_PATH = "/path/to/chromedriver"

DATES = ['2025-12-05', '2025-12-06', '2025-12-07', '2025-12-08', '2025-12-09', '2025-12-10', '2025-12-11']
KEYWORDS = ['Kresge']

# ======== SETUP ========
options = Options()
options.add_argument('--headless')
options.add_argument('--no-sandbox')
options.add_argument('--disable-dev-shm-usage')
driver = webdriver.Chrome(service=Service(CHROMEDRIVER_PATH), options=options)

# ======== NOTIFICATION ========
def send_sms(msg):
    client = Client(TWILIO_SID, TWILIO_AUTH)
    client.messages.create(body=msg, from_=FROM_NUM, to=TO_NUM)

# ======== LOGIN ========
def login_mazevo():
    print("[*] Logging in to Mazevo...")
    driver.get(LOGIN_URL)
    time.sleep(2)

    try:
        # Update these selectors if necessary
        driver.find_element(By.ID, "username").send_keys(USERNAME)
        driver.find_element(By.ID, "password").send_keys(PASSWORD)
        driver.find_element(By.ID, "password").send_keys(Keys.RETURN)
        time.sleep(3)
        print("[+] Login successful.")
    except Exception as e:
        print("[!] Login failed:", e)

# ======== SCRAPE AVAILABILITY ========
def check_availability():
    for date in DATES:
        try:
            url = f"https://events.mit.edu/mazevo/day?date={date}"
            driver.get(url)
            time.sleep(3)
            source = driver.page_source

            if any(keyword in source for keyword in KEYWORDS):
                print(f"[+] Found Kresge availability on {date}")
                send_sms(f"Kresge availability on {date} — check Mazevo.")
            else:
                print(f"[-] No Kresge availability on {date}")
        except Exception as e:
            print(f"[!] Error checking {date}: {e}")

# ======== MAIN LOOP ========
if __name__ == "__main__":
    login_mazevo()
    while True:
        check_availability()
        print("[*] Waiting 10 minutes before next check...")
        time.sleep(600)
