install()
{
    default_install
    cd $PREFIX
    curl -O "https://lsst-web.ncsa.illinois.edu/sim-data/sed_library/seds_170124.tar.gz"
    tar zxvf seds_170124.tar.gz
    rm seds_170124.tar.gz
}
