#!/bin/bash


usage () {
    cat <<EOF
Configure WCT source for building against a UPS products area.
usage:

  wct-configure-for-art-bv.sh [productsdir]

A UPS products directory may be taken from the first entry of
$PRODUCTS or overridden on the command line.  This same directory will
be where the WCT installation is placed.  Detailed external versions
are hard-coded to match the current nominally expected environment.
EOF
    exit
}

products="$1"
set_products () {
    if [ -n "$products" ] ; then
	return
    fi
    IFS=: read -a fields <<<"$PRODUCTS"
    for maybe in ${fields[@]} ; do
	if [ -d "$maybe/boost" ] ; then
	    products="$maybe"
	    return
	fi
    done
    echo "Could not guess where your UPS products are."
    usage
}
set_products

flavor="Linux64bit+4.4-2.23-e14-prof"
lsbrel="$(lsb_release -c)"
case $lsbrel in
    xenial) flavor="Linux64bit+4.4-2.23-e14-prof" ;;
    *) flavor="Linux64bit+4.4-2.23-e14-prof" ;;
esac
	    

# - PRODUCTS

#    --with-tbb=${products}/tbb/v2017_3c/${flavor} \

env CC=gcc CXX=g++ FC=gfortran \
    ./wcb configure \
    --with-tbb=no \
    --with-jsoncpp=${products}/jsoncpp/v1_7_7/${flavor} \
    --with-jsonnet=${products}/jsonnet/v0_9_3/${flavor} \
    --with-eigen=${products}/eigen/v3_3_3 \
    --with-root=${products}/root/v6_08_06g/Linux64bit+4.4-2.23-e14-nu-prof \
    --with-fftw=${products}/fftw/v3_3_6_pl2/Linux64bit+4.4-2.23-prof \
    --with-fftw-include=${products}/fftw/v3_3_6_pl2/Linux64bit+4.4-2.23-prof/include \
    --with-fftw-lib=${products}/fftw/v3_3_6_pl2/Linux64bit+4.4-2.23-prof/lib \
    --boost-includes=${products}/boost/v1_63_0b/${flavor}/include \
    --boost-libs=${products}/boost/v1_63_0b/${flavor}/lib \
    --boost-mt \
    --prefix=install
#    --prefix=${products}/wirecell/v0_6_0dev/${flavor}
