#!/usr/bin/env bash
source ./dj2to3.sh
# 更改虚拟环境的模块 
LIBS_DIR=$VIRTUAL_ENV/lib/python3.3/site-packages

function usage() {
echo "USAGE: $0 python_module_dir_name [...]"
}

if [[ "$@" = "" ]]; then
	usage
	exit 1
fi

pkgs=$@

OLD_IFS="$IFS" 
IFS=" " 
arr=($pkgs) 
IFS="$OLD_IFS" 
for pkg in ${arr[@]} 
do 
	dj2to3 $LIBS_DIR/$pkg
done
