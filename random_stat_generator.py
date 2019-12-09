import numpy as np
import argparse

import cherry_picker.RandomSelect

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("--legend", type=str, default='docs/legends.txt', help="path to NBA legends file")
    cherry_picker.RandomSelect.get_random_player('legend_players.csv')