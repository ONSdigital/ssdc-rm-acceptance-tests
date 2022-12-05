install:
	pipenv install --dev

package_vulnerability:
	PIPENV_PYUP_API_KEY="" pipenv check -i 51499  # Pip Wheel vulnerability, still included with latest pipenv versions from some sources

flake:
	pipenv run flake8 .

vulture:
	pipenv run vulture

lint: flake vulture

check: package_vulnerability lint

test_core: package_vulnerability lint run_tests_core

test: package_vulnerability lint run_tests

run_tests:
	PUBSUB_EMULATOR_HOST=localhost:8538 pipenv run behave acceptance_tests/features

run_tests_core:
	PUBSUB_EMULATOR_HOST=localhost:8538 pipenv run behave acceptance_tests/features --tags="~@regression"

build:
	docker build -t europe-west2-docker.pkg.dev/ssdc-rm-ci/docker/ssdc-rm-acceptance-tests .
