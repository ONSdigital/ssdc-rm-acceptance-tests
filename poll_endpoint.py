import argparse
from time import sleep

from requests.exceptions import ConnectionError, HTTPError

from acceptance_tests.utilities.iap_requests import make_request


def poll_endpoint(url: str, max_retries: int):
    check_endpoint = True
    num_of_retries = 0
    while check_endpoint:
        try:
            response = make_request(url=url)
            response.raise_for_status()
            check_endpoint = False
        except (ConnectionError, HTTPError):
            num_of_retries += 1
            if num_of_retries == max_retries:
                print(f"Reached maximum number of retries on {url}. Stopping script")
                exit(1)

            print(f"{url} is not available. Sleeping for a minute")
            sleep(60)


def parse_arguments():
    parser = argparse.ArgumentParser(
        description="This script polls an endpoint to check if it's available for the"
                    " Acceptance Tests to start running")
    parser.add_argument('--url', help='The url you want to poll', type=str, required=True)
    parser.add_argument('--max_retries', help='Maximum number of retries we want to check URL is up', type=int,
                        required=True)

    return parser.parse_args()


def main():
    args = parse_arguments()
    poll_endpoint(url=args.url, max_retries=args.max_retries)


if __name__ == "__main__":
    main()
