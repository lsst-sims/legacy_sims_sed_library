install()
{
    default_install
    cd $PREFIX
    curl -O "https://lsst-web.ncsa.illinois.edu/sim-data/sed_library/seds_160126.tar.gz"
    tar zxvf seds_160126.tar.gz
    rm seds_160126.tar.gz
}
