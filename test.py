import argparse
from redstamp_extract import get_prediction


parser = argparse.ArgumentParser(description='Extract receive id and receive date from cropped stamp')
parser.add_argument('path', type=str)

if __name__ == '__main__':
    args = parser.parse_args()
    print(get_prediction(open(args.path, 'rb').read()))