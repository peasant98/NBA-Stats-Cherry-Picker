import numpy as np
import argparse

import cherry_picker.RandomSelect as CPRandomSelect

# just some fun generating some random nba player statistics.
if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("--legend", type=str, default='docs/legends.txt', help="path to NBA legends file")
    CPRandomSelect.get_random_player('legend_players.csv')