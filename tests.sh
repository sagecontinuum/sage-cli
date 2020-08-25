#!/bin/bash


# this script tests a few bucket and file operations
# requirements:
# - jq installed
# - SAGE_HOST and SAGE_USER_TOKEN environment variables

fatal() {
  echo -e '\033[0;31m' $* 
  exit 1
}

if [ -z ${SAGE_HOST} ] ; then
    fatal "Environment variable SAGE_HOST not defined"
fi

if [ -z ${SAGE_USER_TOKEN} ] ; then
    fatal "Environment variable SAGE_USER_TOKEN not defined"
fi







set -e
set -x

#check if jq is available:
command -v jq


# create bucket

RESPONSE=$(./sage-cli.py storage bucket create --datatype=training-data)
echo "RESPONSE: ${RESPONSE}"
BUCKET_ID=$(echo "${RESPONSE}" | jq -r '.id')


if [ "${BUCKET_ID}_" == "_" ] ; then
    fatal "BUCKET_IDis empty"
fi

echo "BUCKET_ID=${BUCKET_ID}"


# upload file
./sage-cli.py storage files upload ${BUCKET_ID} ./README.md

# check
FILE_FOUND=$(./sage-cli.py storage files list ${BUCKET_ID} |  jq -r '.[0]')

if [ ${FILE_FOUND}_ != "README.md_" ] ; then
    fatal "file not found"
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
    fatal "permission not found"
fi


# make private again
./sage-cli.py storage permissions delete ${BUCKET_ID} GROUP AllUsers

# check that AllUsers has no permissions
PERM_COUNT=$(./sage-cli.py storage permissions show  d73cae07-0e56-4521-a662-e312def56540 | jq  '.[] | select(.grantee=="AllUsers") ' | wc -l)
if [ ${PERM_COUNT} -ne 0 ] ; then
    fatal "AllUsers still has permissions"
fi


# upload file
FILES_UPLOADED=$(./sage-cli.py storage files upload ${BUCKET_ID} ./README.md | jq '.files_uploaded')
if [ ${FILES_UPLOADED} -ne 1 ] ; then
    fatal "upload failed"
fi

# upload file as another key
FILES_UPLOADED=$(./sage-cli.py storage files upload ${BUCKET_ID} ./README.md --key /directory/test.md | jq '.files_uploaded')
if [ ${FILES_UPLOADED} -ne 1 ] ; then
    fatal "upload failed"
fi
# check was uploaded with correct name
./sage-cli.py storage files list  ${BUCKET_ID} --recursive true | grep "directory/test.md"


#directory upload

echo "test_a" > temp/a.txt

mkdir -p ./temp/dir1/
echo "test_b" > temp/dir1/b.txt
echo "test_c" > temp/dir1/c.txt

mkdir -p ./temp/dir1/dir2/
echo "test_d" > temp/dir1/dir2/d.txt

./sage-cli.py storage files upload ${BUCKET_ID} ./temp --key /dir-test/

LIST=$(./sage-cli.py storage files list ${BUCKET_ID} --prefix /dir-test/ --recursive=true | jq -cS '.')
if [ ${LIST}_ != '["dir-test/temp/a.txt","dir-test/temp/dir1/b.txt","dir-test/temp/dir1/c.txt","dir-test/temp/dir1/dir2/d.txt"]_' ] ; then
    fatal "List of files do not match"
fi




echo "Tests successful."














