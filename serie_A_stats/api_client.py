### **`api_client.py`**

import requests
import configparser

class FootballAPIClient:
    def __init__(self):
        config = configparser.ConfigParser()
        config.read('config.ini')
        self.api_key = config['API']['key']
        self.base_url = "https://api-football-v1.p.rapidapi.com/v3/"
        self.headers = {
            "X-RapidAPI-Key": self.api_key,
            "X-RapidAPI-Host": "api-football-v1.p.rapidapi.com"
        }

    def get_matches(self, league_id: int, date: str) -> dict:
        """Recupera le partite della Serie A per una data specifica."""
        endpoint = f"fixtures?league={league_id}&season=2025&date={date}"
        response = requests.get(f"{self.base_url}{endpoint}", headers=self.headers)
        response.raise_for_status()
        return response.json()
