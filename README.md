# ssdc-rm-acceptance-tests

The Python Behave BDD tests for SSDC RM

## Run the tests locally against ssdc-rm-docker-dev

1. Clone [ssdc-rm-docker-dev](https://github.com/ONSdigital/ssdc-rm-docker-dev) and run `make up` to start the required
   services

2. To Run all the tests:
    ```bash
    make test
    ```

3.  To run just the core tests, those not marked @regression Run:
    ```bash
    make test_core
    ```

## Run tests against a GCP project

Run the `run_gke.sh` bash script.

NB: assumes infrastructure and services exist in respective projects.

To run a locally-modified version of the acceptance tests in a pod you will have to build and tag the image, push it to the GCR and change the image in [acceptance_tests_pod.yml](./acceptance_tests_pod.yml) to point to your modified image
```shell script
IMAGE_TAG=<YOUR_TAG>
make build
docker tag europe-west2-docker.pkg.dev/ssdc-rm-ci/docker/ssdc-rm-acceptance-tests:latest europe-west2-docker.pkg.dev/ssdc-rm-ci/docker/ssdc-rm-acceptance-tests:$IMAGE_TAG
docker push europe-west2-docker.pkg.dev/ssdc-rm-ci/docker/ssdc-rm-acceptance-tests:$IMAGE_TAG
```

Then run the tests with the run GKE script