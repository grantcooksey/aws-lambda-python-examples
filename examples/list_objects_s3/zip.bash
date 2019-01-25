#! /bin/bash

mkdir -p .aws-sam/package
cd .aws-sam/build/$1
zip -r9 ../../package/$1.zip .
