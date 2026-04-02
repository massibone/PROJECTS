def calculate_standings(matches: list) -> list:
    """Calcola la classifica aggiornata."""
    standings = {}
    for match in matches:
        home = match['teams']['home']['name']
        away = match['teams']['away']['name']
        score = match['score']['fulltime']
        if score:
            h_goals, a_goals = map(int, score.split(':'))
            # Aggiorna punti e differenza reti
            standings.setdefault(home, {'points': 0, 'gd': 0})
            standings.setdefault(away, {'points': 0, 'gd': 0})
            if h_goals > a_goals:
                standings[home]['points'] += 3
            elif h_goals == a_goals:
                standings[home]['points'] += 1
                standings[away]['points'] += 1
            else:
                standings[away]['points'] += 3
            standings[home]['gd'] += h_goals - a_goals
            standings[away]['gd'] += a_goals - h_goals
    # Ordina per punti e differenza reti
    return sorted(standings.items(), key=lambda x: (-x[1]['points'], -x[1]['gd']))
