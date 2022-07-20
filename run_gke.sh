#!/bin/bash
set -e

if [ -z "$ENV" ]; then
    echo "No ENV set. Using kubectl current context."

else
    GCP_PROJECT=ssdc-rm-$ENV
    gcloud config set project $GCP_PROJECT
    gcloud container clusters get-credentials rm-k8s-cluster \
        --region europe-west2 \
        --project $GCP_PROJECT
fi

if [ "$NAMESPACE" ]; then
    HTTPS_PROXY=localhost:8888 kubectl config set-context $(HTTPS_PROXY=localhost:8888 kubectl config current-context) --namespace=$NAMESPACE
    echo "NAMESPACE = [$NAMESPACE] Set kubectl namespace for subsequent commands [$NAMESPACE]."
fi
echo "Running RM Acceptance Tests [$(HTTPS_PROXY=localhost:8888 kubectl config current-context)]..."


BEHAVE_TAGS = ''

if ! [ "$REGRESSION" = "false" ]; then
   BEHAVE_TAGS=' --tags=~@regression '
else
    echo "Running with the regression tests"
fi


HTTPS_PROXY=localhost:8888 kubectl delete pod acceptance-tests --wait || true

HTTPS_PROXY=localhost:8888 kubectl apply -f acceptance_tests_pod.yml

HTTPS_PROXY=localhost:8888 kubectl wait --for=condition=Ready pod/acceptance-tests --timeout=200s

HTTPS_PROXY=localhost:8888 kubectl exec -it acceptance-tests -- /bin/bash -c "sleep 2; behave acceptance_tests/features $BEHAVE_TAGS --logging-level WARN"

HTTPS_PROXY=localhost:8888 kubectl delete pod acceptance-tests || true
