# ssdc-rm-acceptance-tests

The Python Behave BDD tests for SSDC RM

## Run the tests locally against ssdc-rm-docker-dev

1. Clone [ssdc-rm-docker-dev](https://github.com/ONSdigital/ssdc-rm-docker-dev) and run `make up` to start the required
   services

2. Run all the RM tests:
    ```shell
    make test
    ```

### Core Tests

To run just the core tests, those not marked @regression Run:

```shell
make run_tests_core
```

### RH Tests

Tests tagged with `@rh` require the RH services. Run these with:

```shell
make run_tests_rh
```

## Run tests against a GCP project

Run the `run_gke.sh` bash script like so, where `ENV` is the environment name suffix in the project name,
like `ssdc-rm-<ENV>`:

```shell
ENV=<YOUR_ENV_SUFFIX> ./run_gke.sh
```

**NB:** assumes infrastructure and RM services exist in respective projects. RH tests are skipped.

By default, this will run the core RM tests, you can run the full suite of RM regression tests with:

```shell
ENV=<YOUR_ENV_SUFFIX> REGRESSION=true ./run_gke.sh
```

### With Local Changes

To run a locally-modified version of the acceptance tests in a pod you will have to build and tag the image, push it to
the GCR and change the image in [acceptance_tests_pod.yml](./acceptance_tests_pod.yml) to point to your modified image tag.

```shell script
IMAGE_TAG=<YOUR_TAG>
make build
docker tag europe-west2-docker.pkg.dev/ssdc-rm-ci/docker/ssdc-rm-acceptance-tests:latest europe-west2-docker.pkg.dev/ssdc-rm-ci/docker/ssdc-rm-acceptance-tests:$IMAGE_TAG
docker push europe-west2-docker.pkg.dev/ssdc-rm-ci/docker/ssdc-rm-acceptance-tests:$IMAGE_TAG
```

Then run the tests with the run GKE script.

## Tests Configuration

Default behave config is provided in [.behaverc](/.behaverc). To run with custom configuration you can edit this file or
override settings with command line args. See the [Using Behave](https://behave.readthedocs.io/en/stable/behave.html)
page for details.

### Running in the IDE

To run the scenarios locally within an IDE you must have the environment variable `PUBSUB_EMULATOR_HOST=localhost:8538`
set.

For Pycharm, a default run configuration template is provided (in [.run](.run)) for the Behave run template, which sets
this variable for you. Providing you are running all the required services already, you should simply be able to run or
debug any feature or scenario within PyCharm without any further configuration.

### Custom Local Test Runs

To run with custom settings locally you will need to set the environment variable `PUBSUB_EMULATOR_HOST=localhost:8538`,
either in your environment or prefacing the call to behave.

The tests can be run by calling the behave command line tool through pipenv (after installing dependencies
with `pipenv install --dev`) like so:

```shell
PUBSUB_EMULATOR_HOST=localhost:8538 pipenv run behave acceptance_tests/features
```

You could alternatively activate the pipenv shell with `pipenv shell` in this project then call the `behave` tool
directly.

This can be uses to run individual feature files from the command line:

```shell
PUBSUB_EMULATOR_HOST=localhost:8538 pipenv run behave acceptance_tests/features/social.feature
```

Or to run with a custom combination of tags like so:

```shell
PUBSUB_EMULATOR_HOST=localhost:8538 pipenv run behave acceptance_tests/features --tags "~@regression" --tags "@rh" 
```

**NOTE** that tags combined in a single arg like  `--tags @foo,@bar` are combined with a logical `OR` whereas tags
provided in multiple args like `--tags @foo --tags @bar` are combined with an `AND`, and multiple negative tags
like `~@foo` can only be combined with `AND` in multiple, separate tags args.
See [Behave Tag Expressions](https://behave.readthedocs.io/en/stable/behave.html#tag-expression).
