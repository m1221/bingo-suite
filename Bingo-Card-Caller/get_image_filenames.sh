#! /bin/bash
# 1. get image file names
# 2. write them to a js file


if [ -z "$1" ]; then
    IMAGE_FOLDER="../source-images/individual-icons"
elif [ "$1" == "p" ]; then
    IMAGE_FOLDER="../private-source-images/individual-icons"
else
    echo "'$1' is not a valid input. Please do not enter an argument OR enter 'p' to get images from '../private-source-images/individual-icons' instead of '../source-images/individual-icons'."
    exit 1
fi

pathnames=""

for filename in $(ls $IMAGE_FOLDER)
    do
        pathname="'../$IMAGE_FOLDER/$filename'"
        if [ "$pathnames" == "" ]; then
            pathnames="\n    $pathname"
        else
            pathnames="$pathnames,\n    $pathname"
        fi
    done

printf "let filepaths = [$pathnames\n];" > "./code/filepaths.js"