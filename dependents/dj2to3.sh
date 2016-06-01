#!/bin/bash
function dj2to3 {
	pkg_dir=$1
	2to3 -w $pkg_dir

	#替换命令ack
	#find $pkg_dir -exec egrep -l "smart_unicode|force_unicde" {} \; | while read read file;
	ack -l "smart_unicode|force_unicode" "$pkg_dir" | while read file;
	do
		# force_unicode and smart_unicode change to "_str" subfix in django.utils.encoding
		sed -ibak2 -e 's/force_unicode/force_str/g;s/smart_unicode/smart_str/g' $file;
	done
}
