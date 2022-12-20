#!/bin/bash

set -e

SCHEMA_REGISTRY_URL=${SCHEMA_REGISTRY_URL:-localhost:3082}
dir=$(dirname $0)

resolved_dir=$(readlink -f $dir)
echo "Registering schemas from $resolved_dir"
cd $resolved_dir

function wrapWithSchemaRegistryMessage() {
    NAME=$1
    cat $NAME.json | jq -R --slurp '{"schema": ., "schemaType": "JSON"}'
}

function createSchema() {
    NAME=$1
    wrapWithSchemaRegistryMessage $NAME | curl -d @- -H "Content-Type: application/vnd.schemaregistry.v1+json" $SCHEMA_REGISTRY_URL/subjects/$NAME/versions -v
}

for file in $(ls *.json); do
  subject=$(basename $file .json)
  createSchema $subject;
done
