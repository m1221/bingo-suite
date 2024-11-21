#! /bin/bash
# 1. get image file names
# 2. write them to a js file
#
# NOTE: this script MUST be run from PROJECT ROOT! 
# Also, the image directory must be a child of the project root director.
# EXAMPLES:
# ./Bingo-Card-Caller/update-filepaths-js.sh
# ./Bingo-Card-Caller/update-filepaths-js.sh ./source-images/individual-icons

if [ -z "$1" ]; then
    IMAGE_FOLDER="./source-images/individual-icons"
elif [ -d "$1" ]; then
    child=$1
    result=$(find "." -type d -wholename "$child")
    if [[ -n $result ]]; then
        IMAGE_FOLDER="$child"
    else
        echo "Please place the image directory inside the project root directory 'BingoSuite'."
        exit 1
    fi
else
    echo "The path \"$1\" does not point to a valid directory."
    exit 1
fi

pathnames=""

for filename in $(ls $IMAGE_FOLDER)
    do
        pathname="'../.$IMAGE_FOLDER/$filename'"
        if [ "$pathnames" == "" ]; then
            pathnames="\n    $pathname"
        else
            pathnames="$pathnames,\n    $pathname"
        fi
    done

printf "let filepaths = [$pathnames\n];\n" > "./Bingo-Card-Caller/code/filepaths.js"