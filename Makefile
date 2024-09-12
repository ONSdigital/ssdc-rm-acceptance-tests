install:
	pipenv install --dev

check_safety:
	PIPENV_PYUP_API_KEY="" pipenv check

flake:
	pipenv run flake8 .

vulture:
	pipenv run vulture

lint: flake vulture

check: check_safety lint

test_core: check lint run_tests_core

test: check lint run_tests

run_tests:
	PUBSUB_EMULATOR_HOST=localhost:8538 pipenv run behave acceptance_tests/features --tags="~@cloud_only"

run_tests_core:
	PUBSUB_EMULATOR_HOST=localhost:8538 pipenv run behave acceptance_tests/features --tags="~@regression" --tags="~@cloud_only"

build:
	docker build -t europe-west2-docker.pkg.dev/ssdc-rm-ci/docker/ssdc-rm-acceptance-tests .
