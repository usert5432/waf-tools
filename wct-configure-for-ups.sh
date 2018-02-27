#!/bin/bash


usage () {
    cat <<EOF
Configure WCT source for building against a UPS products.

  wct-configure-for-art-bv.sh install_directory

This assumes the UPS environment for the dependent products are
already "setup".  

If the install_directory is the string "ups" then the source will be
configured to install into $WIRECELL_FQ_DIR.

EOF
    exit
}

install_dir="$1" ; shift
if [ "$install_dir" = "ups" ] ; then
    install_dir="$WIRECELL_FQ_DIR"
fi


# - PRODUCTS

#    --with-tbb=${products}/tbb/v2017_3c/${flavor} \

env CC=gcc CXX=g++ FC=gfortran \
    ./wcb configure \
    --with-tbb=no \
    --with-jsoncpp="$JSONCPP_FQ_DIR" \
    --with-jsonnet="$JSONNET_FQ_DIR" \
    --with-eigen="$EIGEN_DIR" \
    --with-root="$ROOT_FQ_DIR" \
    --with-fftw="$FFTW_FQ_DIR" \
    --with-fftw-include="$FFTW_INC" \
    --with-fftw-lib="$FFTW_LIB" \
    --boost-includes="$BOOST_INC" \
    --boost-libs="$BOOST_LIB" \
    --boost-mt \
    --prefix="$install_dir"

