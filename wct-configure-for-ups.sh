#!/bin/bash


usage () {
    cat <<EOF
Configure WCT source for building against a UPS products area.
usage:

  wct-configure-for-ups.sh

It is assumed that the calling environment is configured already for a
pre-declared "wirecell" UPS product.  A declaration command goes
something like:

  $ ups declare wirecell <version> \
       -f \$(ups flavor) \
       -q e14:prof \
       -r wirecell/<version> \
       -z /path/to/install/products \
       -U ups  \
       -m wirecell.table

  $ setup wirecell <version> -q e14:prof

This script will then use the UPS environment variables to locate
WCT's dependencies and a "./wcb install" will install into the defined
$WIRECELL_FQ_DIR.  Beware that this will overwrite any existing files
in that directory.
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


env CC=gcc CXX=g++ FC=gfortran \
    ./wcb configure \
    --with-tbb=no \
    --with-jsoncpp=${JSONCPP_FQ_DIR} \
    --with-jsonnet=${JSONNET_FQ_DIR} \
    --with-eigen=${EIGEN_DIR} \
    --with-root=${ROOTSYS} \
    --with-fftw=${FFTW_FQ_DIR} \
    --with-fftw-include=${FFTW_INCLUDE_DIR} \
    --with-fftw-lib=${FFTW_LIBRARY} \
    --boost-includes=${BOOST_INC} \
    --boost-libs=${BOOST_LIB} \
    --boost-mt \
    --prefix=${WIRECELL_FQ_DIR}

