while True:
    try:
        n = int(input("Enter number of teams: "))
        if n < 2:
            print("There must be at least 2 teams")
        else:
            break
    except ValueError:
        print("Enter a valid integer")

teams = []
while len(teams) < n:
    team = input("Enter team name: ").strip()

    if team == "":
        print("Team name cannot be empty")
    elif team.lower() in [t.lower() for t in teams]:
        print("Team already exists")
    else:
        teams.append(team)

matches = []
match_count = {}
total_matches = n * (n - 1)

team_stats = {}

for team in teams:
    team_stats[team] = {
        "played": 0,
        "won": 0,
        "lost": 0,
        "tied": 0,
        "points": 0,
        "runs_scored": 0,
        "runs_conceded": 0,
        "overs_faced": 0,
        "overs_bowled": 0,
        "nrr": 0
    }

for match_number in range(1, total_matches + 1):
    print("\nMatch", match_number)

    while True:
        team1 = input("Enter first team: ").strip()
        team2 = input("Enter second team: ").strip()

        if team1.lower() not in [t.lower() for t in teams]:
            print("First team is not registered")
        elif team2.lower() not in [t.lower() for t in teams]:
            print("Second team is not registered")
        elif team1.lower() == team2.lower():
            print("A team cannot play against itself")
        else:
            team1 = next(t for t in teams if t.lower() == team1.lower())
            team2 = next(t for t in teams if t.lower() == team2.lower())

            pair = tuple(sorted([team1, team2], key=str.lower))

            if match_count.get(pair, 0) >= 2:
                print("These teams have already played twice")
            else:
                break

    while True:
        try:
            runs1 = int(input("Enter runs scored by " + team1 + ": "))
            if runs1 < 0:
                print("Runs cannot be negative")
            else:
                break
        except ValueError:
            print("Enter a valid integer")

    while True:
        try:
            wickets1 = int(input("Enter wickets lost by " + team1 + ": "))
            if wickets1 < 0 or wickets1 > 10:
                print("Wickets must be between 0 and 10")
            else:
                break
        except ValueError:
            print("Enter a valid integer")

    while True:
        try:
            overs1 = int(input("Enter completed overs for " + team1 + ": "))
            balls1 = int(input("Enter remaining balls for " + team1 + " (0-5): "))

            if overs1 < 0 or overs1 > 20:
                print("Overs must be between 0 and 20")
            elif balls1 < 0 or balls1 > 5:
                print("Remaining balls must be between 0 and 5")
            elif overs1 == 20 and balls1 != 0:
                print("At 20 overs, remaining balls must be 0")
            elif overs1 * 6 + balls1 == 0:
                print("An innings must have at least one legal ball")
            else:
                break
        except ValueError:
            print("Enter valid integers")

    while True:
        try:
            runs2 = int(input("Enter runs scored by " + team2 + ": "))
            if runs2 < 0:
                print("Runs cannot be negative")
            else:
                break
        except ValueError:
            print("Enter a valid integer")

    while True:
        try:
            wickets2 = int(input("Enter wickets lost by " + team2 + ": "))
            if wickets2 < 0 or wickets2 > 10:
                print("Wickets must be between 0 and 10")
            else:
                break
        except ValueError:
            print("Enter a valid integer")

    while True:
        try:
            overs2 = int(input("Enter completed overs for " + team2 + ": "))
            balls2 = int(input("Enter remaining balls for " + team2 + " (0-5): "))

            if overs2 < 0 or overs2 > 20:
                print("Overs must be between 0 and 20")
            elif balls2 < 0 or balls2 > 5:
                print("Remaining balls must be between 0 and 5")
            elif overs2 == 20 and balls2 != 0:
                print("At 20 overs, remaining balls must be 0")
            elif overs2 * 6 + balls2 == 0:
                print("An innings must have at least one legal ball")
            else:
                break
        except ValueError:
            print("Enter valid integers")

    if wickets1 == 10 and overs1 * 6 + balls1 < 120:
        adjusted_overs1 = 20
    else:
        adjusted_overs1 = (overs1 * 6 + balls1) / 6

    if wickets2 == 10 and overs2 * 6 + balls2 < 120:
        adjusted_overs2 = 20
    else:
        adjusted_overs2 = (overs2 * 6 + balls2) / 6

    matches.append((
        team1, team2, runs1, runs2,
        adjusted_overs1, adjusted_overs2
    ))

    match_count[pair] = match_count.get(pair, 0) + 1

    stats1 = team_stats[team1]
    stats2 = team_stats[team2]

    stats1["played"] += 1
    stats2["played"] += 1

    stats1["runs_scored"] += runs1
    stats1["runs_conceded"] += runs2

    stats2["runs_scored"] += runs2
    stats2["runs_conceded"] += runs1

    stats1["overs_faced"] += adjusted_overs1
    stats1["overs_bowled"] += adjusted_overs2

    stats2["overs_faced"] += adjusted_overs2
    stats2["overs_bowled"] += adjusted_overs1

    if runs1 > runs2:
        stats1["won"] += 1
        stats1["points"] += 2
        stats2["lost"] += 1
    elif runs2 > runs1:
        stats2["won"] += 1
        stats2["points"] += 2
        stats1["lost"] += 1
    else:
        stats1["tied"] += 1
        stats2["tied"] += 1
        stats1["points"] += 1
        stats2["points"] += 1

    print("Match details saved")

tournament_complete = True

for team1 in teams:
    for team2 in teams:
        if team1 != team2:
            pair = tuple(sorted([team1, team2], key=str.lower))
            if match_count.get(pair, 0) != 2:
                tournament_complete = False
                break
    if not tournament_complete:
        break

if tournament_complete:
    print("\nTournament completed successfully")
else:
    print("\nTournament is incomplete")

for team in teams:
    stats = team_stats[team]

    if stats["overs_faced"] > 0 and stats["overs_bowled"] > 0:
        stats["nrr"] = (
            stats["runs_scored"] / stats["overs_faced"]
            - stats["runs_conceded"] / stats["overs_bowled"]
        )

sortings = sorted(
    team_stats.items(),
    key=lambda item: (item[1]["points"], item[1]["nrr"]),
    reverse=True
)

print("\n************ FINAL SUMMARY **************")
for rank, (team, stats) in enumerate(sortings, start=1):
    print("\nPosition:", rank)
    print("Team:", team)
    print("Matches Played:", stats["played"])
    print("Won:", stats["won"])
    print("Lost:", stats["lost"])
    print("Tied:", stats["tied"])
    print("Points:", stats["points"])
    print("Runs Scored:", stats["runs_scored"])
    print("Runs Given:", stats["runs_conceded"])
    print("Overs Faced:", round(stats["overs_faced"], 3))
    print("Overs Bowled:", round(stats["overs_bowled"], 3))
    print("Net Run Rate:", round(stats["nrr"], 3))

