#!/bin/bash


# this script tests a few bucket and file operations
# requirements:
# - jq installed
# - SAGE_HOST and SAGE_USER_TOKEN environment variables


if [ -z ${SAGE_HOST} ] ; then
    echo "Environment variable SAGE_HOST not defined"
    exit 1
fi

if [ -z ${SAGE_USER_TOKEN} ] ; then
    echo "Environment variable SAGE_USER_TOKEN not defined"
    exit 1
fi

set -e
set -x

#check if jq is available:
command -v jq


# create bucket


BUCKET_ID=$(./sage-cli.py storage bucket create --datatype=training-data | jq -r '.id')

echo "BUCKET_ID=${BUCKET_ID}"


# upload file
./sage-cli.py storage files upload ${BUCKET_ID} ./README.md

# check
FILE_FOUND=$(./sage-cli.py storage files list ${BUCKET_ID} |  jq -r '.[0]')

if [ ${FILE_FOUND}_ != "README.md_" ] ; then
    echo "file not found"
    exit 1
fi


# download file 
mkdir -p temp/
./sage-cli.py storage files download ${BUCKET_ID} README.md --target temp/test.md

# compare downloaded file with original
diff --brief README.md temp/test.md

rm temp/test.md


# make bucket public
./sage-cli.py storage permissions public ${BUCKET_ID}

# check it is public (matching permission object has 3 fields, this is what we use to test the match)
FIELD_COUNT=$(./sage-cli.py storage permissions show ${BUCKET_ID} | jq  '.[] | select(.grantee=="AllUsers") | select(.permission=="READ") | length')

if [ ${FIELD_COUNT} -ne 3 ] ; then
    echo "permission not found"
    exit 1
fi


# make private again
./sage-cli.py storage permissions delete ${BUCKET_ID} GROUP AllUsers

# check that AllUsers has no permissions
PERM_COUNT=$(./sage-cli.py storage permissions show  d73cae07-0e56-4521-a662-e312def56540 | jq  '.[] | select(.grantee=="AllUsers") ' | wc -l)
if [ ${PERM_COUNT} -ne 0 ] ; then
    echo "AllUsers still has permissions"
    exit 1
fi



# upload file as another key
./sage-cli.py storage files upload ${BUCKET_ID} ./README.md --key /directory/test.md

sage-cli.py storage files list  ${BUCKET_ID} --recursive true | grep "directory/test.md"


echo "Tests successful."














