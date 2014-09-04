install()
{
    default_install
    cd $PREFIX
    curl -O "http://lsst-web.ncsa.illinois.edu/~krughoff/data/seds_090414.tar.gz"
    tar zxvf seds_090414.tar.gz
    rm seds_090414.tar.gz
}
