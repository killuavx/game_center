#!/usr/bin/env bash

URL_MACOSX=https://phantomjs.googlecode.com/files/phantomjs-1.9.2-macosx.zip
URL_LINUX_X86_64=https://phantomjs.googlecode.com/files/phantomjs-1.9.2-linux-x86_64.tar.bz2
URL_LINUX_I686=https://phantomjs.googlecode.com/files/phantomjs-1.9.2-linux-i686.tar.bz2

function install_phantomjs()
{
    url=$1
    file_name=`basename $url`
    file_ext=${file_name##*.}
    _dir_name=${file_name%.*}
    if [ "$file_ext" == "bz2" ];
    then
        dir_name=${_dir_name%.*}
        file_ext=${file_name##*.}
    else
        dir_name=$_dir_name
    fi

    wget -np -nd --no-check-certificate $url -O $file_name

    case $file_ext in
        bz2)
            tar jxvf $file_name
            ;;
        zip)
            unzip $file_name
            ;;
    esac

    cp $dir_name/bin/phantomjs $VIRTUAL_ENV/bin
}
