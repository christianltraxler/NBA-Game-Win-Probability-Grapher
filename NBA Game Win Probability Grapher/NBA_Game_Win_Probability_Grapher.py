# nba_api imports
from nba_api.stats.endpoints import winprobabilitypbp
from nba_api.stats.endpoints import leaguegamefinder
from nba_api.stats.static import teams

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

import win_probability_graph as wpg


# get_team_id: team_abbreviation
def get_team_id(team_abbreviation):
    # Get all the teams
    nba_teams = teams.get_teams()

    # Search for team based on abbreviation
    if (team_abbreviation != ''):
        team_to_find = [team for team in nba_teams if team['abbreviation'] == team_abbreviation][0]
    else:
        return None;

    # Get team_id based on team
    team_id = team_to_find['id']

    # Return team_id
    return team_id

# get_game_info: team_id, vs_team_id
def get_game_info(date, team_id, vs_team_id):
    # Search For Game
    gamefinder = leaguegamefinder.LeagueGameFinder(team_id_nullable=team_id, vs_team_id_nullable=vs_team_id, date_from_nullable=date,date_to_nullable=date)

    # Get dict based on games
    games_dict = gamefinder.get_normalized_dict()

    # Get the first game
    games = games_dict['LeagueGameFinderResults']
    game = games[0]
    
    # Return the game
    return game


def get_game_seconds(play):
    return ((720.0 - play['SECONDS_REMAINING']) + 720.0*(play['PERIOD']-1))/720


if __name__ == "__main__":

    # Get the info about the game
    print('Enter the date of the game:')
    game_date = input()
    print('Enter a team:')
    team = input()
    print('Optional: Enter the other team:')
    vs_team = input()

    # Get the info about the game
    game_info = get_game_info(date=game_date,team_id=get_team_id(team),vs_team_id=get_team_id(vs_team))

    # Create and Setup the Win Probability Graph
    graph = wpg.WinProbabilityGraph(game_info)
    graph.setup()

    # Show the graph
    plt.show()