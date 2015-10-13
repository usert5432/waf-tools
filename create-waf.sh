#!/bin/bash

target=$1 ; shift
if [ -n "$target" ] ; then
    target="$(readlink -f $(dirname $target))/$(basename $target)"
fi

tools="eigen3 rootsys smplpkgs"

wtdir=$(dirname $(readlink -f $BASH_SOURCE))
echo "wtdir is $wtdir"
wafdir=$(readlink -f ../waf)
echo "wafdir is $wafdir"
if [ ! -d $wafdir ] ; then
    echo "This script assumes waf dir at $wafdir"
    exit 1
fi

toolflags="compat15,doxygen,boost,bjam"
for tool in $tools ;
do
    toolflags="$toolflags,${wtdir}/${tool}.py"
done

cd $wafdir
echo "Building waf in $(pwd)"

echo "python waf-light --tools=$toolflags"
python waf-light --tools=$toolflags
if [ -n "$target" ] ; then
    cp waf $target
else
    echo "New waf is:"
    echo "$(readlink -f waf)"
fi


