# nba_api imports
from nba_api.stats.endpoints import winprobabilitypbp
from nba_api.stats.endpoints import leaguegamefinder

import matplotlib.pyplot as plt
import NBA_Game_Win_Probability_Grapher as WPG

class WinProbabilityGraph:
    def __init__(self, game_info):
        self.game_info = game_info
        self.game_id = game_info['GAME_ID']
        self.fig = plt.figure()
        self.ax = self.fig.add_subplot()
        self.info = self.fig.add_subplot()
        self.x, self.y, self.winprobpbp_dict = self.get_values()


    def get_values(self):
        # Get the Win Probability Play By Play for the game
        game_winprobpbp = winprobabilitypbp.WinProbabilityPBP(game_id=self.game_id)

        # Get the dict for the Win Probability
        winprobpbp_dict = game_winprobpbp.get_normalized_dict()

        x = []
        y = []
        # For each play/second add x: Seconds, y: Win Probability Percent
        for play in winprobpbp_dict['WinProbPBP']:
            x.append(WPG.get_game_seconds(play))
            # Determine the percentage to plot based on the first team entered
            if ('@' in self.game_info['MATCHUP']):
                y.append(1 - play['HOME_PCT'])
            else:
                y.append(play['HOME_PCT'])
        return x, y, winprobpbp_dict


    def setup(self):
        # Plot x and y on to the axes
        self.ax.plot(self.x, self.y)

        # Add to the axes
        self.ax.set_title(self.game_info['MATCHUP'] + ' (' + self.game_info['GAME_DATE'] + ') Win Probability Over Time')
        self.ax.set_xlabel('Periods')
        self.ax.xaxis.set_major_locator(plt.MultipleLocator(1))
        self.ax.set_ylabel('Home Win Probability')
        self.ax.set_ylim(0,1)
        