install()
{
    default_install
    cd $PREFIX
    curl -O "http://lsst-web.ncsa.illinois.edu/~krughoff/data/seds_100614.tar.gz"
    tar zxvf seds_090814.tar.gz
    rm seds_090814.tar.gz
}
