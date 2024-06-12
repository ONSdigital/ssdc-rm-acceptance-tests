import argparse
from time import sleep

from requests.exceptions import ConnectionError, HTTPError

from acceptance_tests.utilities.iap_requests import make_request


def healthcheck(url: str, max_retries: int):
    check_support_tool = True
    num_of_retries = 0
    while check_support_tool:
        try:
            response = make_request(url=url)
            response.raise_for_status()
            check_support_tool = False
        except (ConnectionError, HTTPError):
            num_of_retries += 1
            if num_of_retries > max_retries:
                print("Reached Maximum number of retries. Stopping script")
                break
            print("Support Tool not available. Sleeping for a minute")
            sleep(2)


def parse_arguments():
    parser = argparse.ArgumentParser(description='Check support tool is up and running')
    parser.add_argument('--url', help='The Support Tool url to pass in', type=str, required=True)
    parser.add_argument('--max_retries', help='Maximum number of retries we want to check support tool is up', type=int,
                        required=True)

    return parser.parse_args()


def main():
    args = parse_arguments()
    healthcheck(url=args.url, max_retries=args.max_retries)


if __name__ == "__main__":
    main()
