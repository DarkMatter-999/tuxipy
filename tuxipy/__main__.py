import argparse
from .tuxi import main

parser = argparse.ArgumentParser(prog='tuxipy')

parser.add_argument('q', nargs='?', help='Search query')
parser.add_argument('--query', nargs='?', help='Search query')

args = parser.parse_args()

if __name__ == '__main__':
    main(args)