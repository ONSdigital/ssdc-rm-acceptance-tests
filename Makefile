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

test: package_vulnerability lint at_tests

at_tests:
	PUBSUB_EMULATOR_HOST=localhost:8538 pipenv run python run.py --log_level WARN

build:
	docker build -t eu.gcr.io/ssdc-rm-ci/rm/ssdc-rm-acceptance-tests .