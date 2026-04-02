from api_client import FootballAPIClient
from data_processor import calculate_standings
from csv_exporter import export_to_csv
import argparse
from datetime import datetime

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--date", type=str, default=datetime.now().strftime("%Y-%m-%d"),
                        help="Data delle partite (YYYY-MM-DD)")
    args = parser.parse_args()

    client = FootballAPIClient()
    matches = client.get_matches(league_id=135, date=args.date)  # 135 = Serie A
    standings = calculate_standings(matches['response'])

    filename = f"output/risultati_seriea_{args.date.replace('-', '')}.csv"
    export_to_csv(matches['response'], standings, filename)
    print(f"Dati esportati in {filename}")

if __name__ == "__main__":
    main()
