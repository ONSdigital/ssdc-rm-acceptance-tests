install:
	pipenv install --dev

package_vulnerability:
	PIPENV_PYUP_API_KEY="" pipenv check

flake:
	pipenv run flake8 .

vulture:
	pipenv run vulture

lint: flake vulture

check: package_vulnerability lint

test_core: package_vulnerability lint at_tests_core

test: package_vulnerability lint at_tests

at_tests:
	PUBSUB_EMULATOR_HOST=localhost:8538 pipenv run python run.py --log_level WARN

at_tests_core:
	PUBSUB_EMULATOR_HOST=localhost:8538 pipenv run python run.py --log_level WARN --tags="~@regression"

build:
	docker build -t europe-west2-docker.pkg.dev/ssdc-rm-ci/docker/ssdc-rm-acceptance-tests .