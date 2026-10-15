# Set the container runtime based on architecture, default to docker for amd64 and podman for arm64
DOCKER ?= $(shell if [ "$$(uname -m)" = "arm64" ]; then echo podman; else echo docker; fi)

install:
	pipenv install --dev

flake:
	pipenv run flake8 .

vulture:
	pipenv run vulture

lint: flake vulture


test_core: lint run_tests_core

test: lint run_tests

run_tests:
	PUBSUB_EMULATOR_HOST=localhost:8538 pipenv run behave acceptance_tests/features --tags="~@cloud_only"

run_tests_core:
	PUBSUB_EMULATOR_HOST=localhost:8538 pipenv run behave acceptance_tests/features --tags="~@regression" --tags="~@cloud_only"

build:
	$(DOCKER) build --platform linux/amd64 -t europe-west2-docker.pkg.dev/ssdc-rm-ci/docker/ssdc-rm-acceptance-tests .

megalint:  ## Run the mega-linter. v10.1.0
	$(DOCKER) run --platform linux/amd64 --rm \
		-v /var/run/docker.sock:/var/run/docker.sock:rw \
		-v $(shell pwd):/tmp/lint:rw \
		gchr.io/oxsecurity/megalinter:b09486c423063200d6f203b63121e0967719eee03c234844f6f1dd658f00a31b 

megalint-fix:  ## Run the mega-linter and attempt to auto fix any issues. v10.1.0
	$(DOCKER) run --platform linux/amd64 --rm \
		-v /var/run/docker.sock:/var/run/docker.sock:rw \
		-v $(shell pwd):/tmp/lint:rw \
		-e APPLY_FIXES=all \
		gchr.io/oxsecurity/megalinter:b09486c423063200d6f203b63121e0967719eee03c234844f6f1dd658f00a31b 

clean_megalint: ## Clean the temporary files.
	rm -rf megalinter-reports

lint_check: clean_megalint megalint