import argparse
from time import sleep

import requests

from acceptance_tests.utilities.iap_requests import make_request


def healthcheck(url: str):
    retry = True
    while retry:
        try:
            response = make_request(url=url)
            response.raise_for_status()
            retry = False
        except requests.exceptions.ConnectionError:
            print("Support Tool not available. Sleeping for a minute")
            sleep(60)


def parse_arguments():
    parser = argparse.ArgumentParser(description='Check support tool is up and running')
    parser.add_argument('--url', help='Path to sample schema file', type=str, required=True)

    return parser.parse_args()


def main():
    args = parse_arguments()
    healthcheck(url=args.url)


if __name__ == "__main__":
    main()
