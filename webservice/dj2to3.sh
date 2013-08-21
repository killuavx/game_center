#!/bash/sh
pkg_dir = $1
2to3 -w $pkg_dir
ack -l "smart_unicode|force_unicode" $pkg_dir | while read file;
do
   sed -i -e 's/force_unicode/force_str/g;s/smart_unicode/smart_str/g' $file;
done
