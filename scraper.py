import re
from curl_cffi import requests

class SofaScraper:
    def __init__(self):
        # Using chrome impersonation to handle TLS fingerprinting
        self.session = requests.Session(impersonate="chrome")
        self.session.headers.update({
            'Origin': 'https://www.sofascore.com',
            'Referer': 'https://www.sofascore.com/',
            'Accept': '*/*',
            'Accept-Language': 'en-US,en;q=0.9',
            'Cache-Control': 'no-cache'
        })

    def extract_event_id(self, url):
        """Finds the event ID in the URL string using regex patterns."""
        match = re.search(r'#id:(\d+)', url)
        if match: return match.group(1)
        match = re.search(r'/(\d{7,8})/', url)
        if match: return match.group(1)
        match = re.search(r'\d{7,}', url)
        return match.group(0) if match else None

    def fetch_lineups(self, event_id):
        """Fetches the game lineup and stats from the API."""
        url = f"https://api.sofascore.com/api/v1/event/{event_id}/lineups"
        try:
            response = self.session.get(url)
            if response.status_code == 200:
                return response.json()
            return None
        except Exception as e:
            print(f"Network Error: {e}")
            return None