import re

def new_player():
    return { "FG" : 0, # Field Goal <-- done
             "FGA" : 0, # Field Goal Attempt <-- done
             "FG%" : [], # Field Goal Percentage <-- done
             "3P" :  0, # 3-Point Field Goals <-- done
             "3PA" : 0, # 3-Point Attempt <-- done
             "3P%" : [], # 3-Point Percentage <-- done
             "FT" :  0, # Free Throw Made <-- done
             "FTA" : 0, # Free Throw Attempt <-- done
             "FT%" : [], # Free Throw Percentage <-- done
             "ORB" : 0, # Offensive Rebounds By Team <-- done
             "DRB" : 0, # Defensive Rebounds By Team <-- done
             "TRB" : 0, # Total Rebounds
             "AST" : 0, # Assists <-- done
             "STL" : 0, # Steals <-- done
             "BLK" : 0, # Blocks <-- done
             "TOV" : 0, # Turnovers <-- done
             "PF" :  0, # Personal Foul <-- done
             "PTS" : 0 # Points <-- done
            }

def get_average(array):
    if len(array) > 0:
        return round((sum(array) / len(array)) * 100, 2)
    else:
        return 0

def print_final_result(both_teams_data):
#    print(both_teams_data)

    final_team = {'FG': 0, 'FGA': 0, 'FG%': [], '3P': 0, '3PA': 0, '3P%': [], 'FT': 0, 'FTA': 0, 'FT%': [], 'ORB': 0, 'DRB': 0, 'TRB': 0,
    'AST': 0, 'STL': 0, 'BLK': 0, 'TOV' : 0, "PF": 0, 'PTS': 0}

    print("Players\t\tFG\tFGA\tFG%\t3P\t3PA\t3P%\tFT\tFTA\tFT%\tORB\tDRB\tTRB\tAST\tSTL\tBLK\tTOV\tPF\tPTS")
    for player_name, data in both_teams_data['home_team']['players_data'].items():
        print('{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}'.format(player_name, 
        data['FG'], data['FGA'], get_average(data['FG%']), data['3P'], data['3PA'], get_average(data['3P%']), data['FT'], data['FTA'], get_average(data['FT%']), data['ORB'], data['DRB'], data['TRB'], data['AST'], data['STL'], data['BLK'], data['TOV'], data['PF'], data['PTS']))
        
        final_team['FG'] += data['FG']
        final_team['FGA'] += data['FGA']
        final_team['FG%'] += data['FG%']
        final_team['3P'] += data['3P']
        final_team['3PA'] += data['3PA']
        final_team['3P%'] += data['3P%']
        final_team['FT'] += data['FT']
        final_team['FTA'] += data['FTA']
        final_team['FT%'] += data['FT%']
        final_team['ORB'] += data['ORB']
        final_team['DRB'] += data['DRB']
        final_team['TRB'] += data['TRB']
        final_team['AST'] += data['AST']
        final_team['STL'] += data['STL']
        final_team['BLK'] += data['BLK']
        final_team['TOV'] += data['TOV']
        final_team['PF'] += data['PF']
        final_team['PTS'] += data['PTS']

    print("Team Totals \t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}".format(final_team['FG'], final_team['FGA'], 
    get_average(final_team['FG%']), final_team['3P'], final_team['3PA'], get_average(final_team['3P%']), final_team['FT'], final_team['FTA'], 
    get_average(final_team['FT%']), final_team['ORB'], final_team['DRB'], final_team['TRB'], final_team['AST'], final_team['STL'], 
    final_team['BLK'], final_team['TOV'], final_team['PF'], final_team['PTS']))

def analyse_nba_game(play_by_play_moves):
    # Necessary for all
    nba_game_blazers_lakers = open(play_by_play_moves, "r")
    read_dataset1 = (nba_game_blazers_lakers.readline())

    both_teams_data = {
        "home_team" : {
            "name": "", 
            "players_data" : {}
        },
        "away_team" : {
            "name": "", 
            "players_data": {}
        }
    }

    # print(read_dataset1)

    def which_team(game): # game = read_dataset1
        if game[4] == game[2]:
            return "home_team"
        elif game[3] == game[2]:
            return "away_team"

    def get_player_name(both_teams_data, current_team, current_play, regex_str):
        player_name = re.findall(regex_str, current_play)[0].strip(" ")
        if (both_teams_data[current_team]['players_data'].get(player_name) == None):
            both_teams_data[current_team]['players_data'][player_name] = new_player()
            if (both_teams_data[current_team]['players_data'].get(player_name) == "Team"):
                print("")
        return player_name


    def parse_line(current_line, both_teams_data):
        splitted_read_dataset1 = current_line.split("|")

        both_teams_data["away_team"]["name"] = splitted_read_dataset1[3] # 
        # print(both_teams_data["away_team"]["name"])
        both_teams_data["home_team"]["name"] = splitted_read_dataset1[4]
        # print(both_teams_data["home_team"]["name"])
        current_play = splitted_read_dataset1[7]
        #print(current_play)
        relevant_team = splitted_read_dataset1[2]
        current_team = which_team(splitted_read_dataset1)

        if (re.findall(".* by Team", current_play)):
            pass
        elif (re.findall("(.*) misses 2-pt", current_play)): # 2-pt miss
            FGA_test = {"current_team" : 'FGA'}
            player_name = get_player_name(both_teams_data, current_team, current_play, "(.*) misses 2-pt")
            both_teams_data[current_team]['players_data'][player_name]["FG%"].append(0)
            both_teams_data[current_team]['players_data'][player_name]["FGA"] += 1
        elif (re.findall("(.*) makes 2-pt", current_play)): # 2-pt made
            player_name = get_player_name(both_teams_data, current_team, current_play, "(.*) makes 2-pt")
            both_teams_data[current_team]['players_data'][player_name]["FGA"] += 1
            both_teams_data[current_team]['players_data'][player_name]["PTS"] += 2
            both_teams_data[current_team]['players_data'][player_name]["FG"] += 2
            both_teams_data[current_team]['players_data'][player_name]["FG%"].append(1)             
        elif (re.findall("Defensive rebound by (.*)", current_play)): # defensive rebound
            player_name = get_player_name(both_teams_data, current_team, current_play, "Defensive rebound by (.*)")
            DRB_test = {"current_team" : 'DRB'}
            TOV_test = {"current_team" : 'TOV'}
            both_teams_data[current_team]['players_data'][player_name]["DRB"] += 1
            both_teams_data[current_team]['players_data'][player_name]["TOV"] += 1
        elif (re.findall("Offensive rebound by (.*)", current_play)): # offensive rebound
            player_name = get_player_name(both_teams_data, current_team, current_play, "Offensive rebound by (.*)")
            ORB_test = {"current_team" : 'ORB'}
            both_teams_data[current_team]['players_data'][player_name]["ORB"] += 1
            both_teams_data[current_team]['players_data'][player_name]["TOV"] += 1
        elif (re.findall("(.*) misses 3-pt", current_play)): # 3-pt miss
            player_name = get_player_name(both_teams_data, current_team, current_play, "(.*) misses 3-pt")
            TPA_test = {"current_team" : '3PA'}
            both_teams_data[current_team]['players_data'][player_name]["3P%"].append(0)
            both_teams_data[current_team]['players_data'][player_name]["FGA"] += 1
        elif (re.findall("(.*) makes 3-pt", current_play)): # 3-pt made
            player_name = get_player_name(both_teams_data, current_team, current_play, "(.*) makes 3-pt")
            both_teams_data[current_team]['players_data'][player_name]["3PA"] += 1
            both_teams_data[current_team]['players_data'][player_name]["PTS"] += 3
            both_teams_data[current_team]['players_data'][player_name]["3P"]  += 3              
            both_teams_data[current_team]['players_data'][player_name]["3P%"].append(1)
        elif(re.findall("(.*) misses free throw", current_play)): # free-throw miss
            FTA_test = {"current_team" : 'FTA'}
            player_name = get_player_name(both_teams_data, current_team, current_play, "(.*) misses free throw")
            both_teams_data[current_team]['players_data'][player_name]["FT%"].append(0)
            both_teams_data[current_team]['players_data'][player_name]["FTA"] += 1
        elif (re.findall("(.*) makes free throw", current_play)): # free throw made
            FT_test = {"current_team" : 'FT'}
            player_name = get_player_name(both_teams_data, current_team, current_play, "(.*) makes free throw")
            both_teams_data[current_team]['players_data'][player_name]["FTA"] += 1
            both_teams_data[current_team]['players_data'][player_name]["PTS"] += 1
            both_teams_data[current_team]['players_data'][player_name]["FT"]  += 1 
            both_teams_data[current_team]['players_data'][player_name]["FT%"].append(1)
        elif (re.findall("assist by ([^\)]*)", current_play)): # assist
            AST_test = {"current_team" : 'AST'}
            player_name = get_player_name(both_teams_data, current_team, current_play, "assist by ([^\)]*)")
            both_teams_data[current_team]['players_data'][player_name]["AST"] += 1
        elif (re.findall("steal by ([^\)]*)", current_play)): # steal
            STL_test = {"current_team" : 'STL'}
            player_name = get_player_name(both_teams_data, current_team, current_play, "steal by ([^\)]*)")
            both_teams_data[current_team]['players_data'][player_name]["STL"] += 1
        elif (re.findall("block by ([^\)]*)", current_play)): # block
            BLK_test = {"current_team" : 'BLK'}
            player_name = get_player_name(both_teams_data, current_team, current_play, "block by ([^\)]*)")
            both_teams_data[current_team]['players_data'][player_name]["BLK"] += 1
        elif (re.findall("Personal foul by ([^\(]*)", current_play)): # personal foul
            PF_test = {"current_team" : 'PF'}
            player_name = get_player_name(both_teams_data, current_team, current_play, "Personal foul by ([^\(]*)")
            both_teams_data[current_team]['players_data'][player_name]["PF"] += 1


    for current_line in nba_game_blazers_lakers:
        # print(current_line.split('|'))
        parse_line(current_line, both_teams_data)
    
    print_final_result(both_teams_data)

    exit

analyse_nba_game("nba_game_blazers_lakers.txt")
# print(nba_game_blazers_lakers)
