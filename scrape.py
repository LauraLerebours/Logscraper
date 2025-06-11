import requests
from bs4 import BeautifulSoup
import schedule
import time
from twilio.rest import Client

# Twilio configuration
TWILIO_SID = 'your_twilio_sid'
TWILIO_AUTH_TOKEN = 'your_auth_token'
TWILIO_PHONE_NUMBER = 'your_twilio_number'
TO_PHONE_NUMBER = 'your_boss_number'

# Monitor configuration
DATE_RANGE = ['2025-12-05', '2025-12-06', '2025-12-07', '2025-12-08', '2025-12-09', '2025-12-10', '2025-12-11']
KRESGE_KEYWORDS = ['Kresge']

# Optional: headers if Mazevo checks user-agent
HEADERS = {
    'User-Agent': 'Mozilla/5.0'
}

def send_sms(message):
    client = Client(TWILIO_SID, TWILIO_AUTH_TOKEN)
    client.messages.create(
        body=message,
        from_=TWILIO_PHONE_NUMBER,
        to=TO_PHONE_NUMBER
    )

def check_mazevo():
    print("Checking Mazevo...")
    for date in DATE_RANGE:
        url = f"https://events.mit.edu/mazevo/day?date={date}"  # example, may vary
        try:
            response = requests.get(url, headers=HEADERS)
            soup = BeautifulSoup(response.text, 'html.parser')

            # Find all entries that mention "Kresge" (may vary based on structure)
            results = soup.find_all(text=lambda text: text and any(kw in text for kw in KRESGE_KEYWORDS))

            if results:
                send_sms(f"Kresge availability found on {date}!")
                print(f"Availability found for {date}")
            else:
                print(f"No availability on {date}")
        except Exception as e:
            print(f"Error on {date}: {e}")

# Run every 10 minutes
schedule.every(10).minutes.do(check_mazevo)

print("Starting scraper...")
while True:
    schedule.run_pending()
    time.sleep(1)
