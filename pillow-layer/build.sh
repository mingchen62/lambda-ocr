#!/bin/bash

if [ "$#" -ne 1 ]; then
    echo "please provide python package name, for example, pillow"
    exit
fi

export PKG_DIR="python"

rm -rf ${PKG_DIR} && mkdir -p ${PKG_DIR}

docker run --rm -v $(pwd):/pkg_dir -w /pkg_dir lambci/lambda:build-python3.6 \
    pip install $1 -t ${PKG_DIR}/lib/python3.6/site-packages

# use serverless to build and deploy
rm -rf layer && mkdir -p layer
mv python layer/
serverless package
serverless deploy

# for manually build layer
#pkg_name="python36-"$1".zip" 
#echo "${pkg_name}"
#zip -r "${pkg_name}" .
#unzip -l "${pkg_name}"

