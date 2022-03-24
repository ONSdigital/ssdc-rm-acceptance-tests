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
    kubectl config set-context $(kubectl config current-context) --namespace=$NAMESPACE
    echo "NAMESPACE = [$NAMESPACE] Set kubectl namespace for subsequent commands [$NAMESPACE]."
fi
echo "Running RM Acceptance Tests [$(kubectl config current-context)]..."


BEHAVE_TAGS=''

if ! [ "$REGRESSION" = "true" ]; then
    BEHAVE_TAGS=' --tags=~@regression'
else
    echo "Running with the regression tests"
fi


kubectl delete pod acceptance-tests --wait || true

kubectl apply -f acceptance_tests_pod.yml

kubectl wait --for=condition=Ready pod/acceptance-tests --timeout=200s

kubectl exec -it acceptance-tests -- /bin/bash -c "sleep 2; behave acceptance_tests/features $BEHAVE_TAGS --no-logcapture --logging-level WARN"

kubectl delete pod acceptance-tests || true
