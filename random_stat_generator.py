import numpy as np
import argparse

import cherry_picker.RandomSelect as CPRandomSelect

# just some fun generating some random nba player statistics.
if __name__ == '__main__':
    CPRandomSelect.get_random_player(np.random.choice(['legend_players.csv', 'all_players.csv']))