#!/bin/bash



rootdir="rootdir"



if [ "$1" == "" ]; then
    exit 0

elif [ $1 == $rootdir ]; then
    dir=$(cd $(dirname $0); pwd)
    echo "${dir}/"
    exit 1
    
fi
