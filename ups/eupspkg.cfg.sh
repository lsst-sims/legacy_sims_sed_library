install()
{
    default_install
    cd $PREFIX
    curl -O "http://lsst-web.ncsa.illinois.edu/~krughoff/data/seds_100614.tar.gz"
    tar zxvf seds_100614.tar.gz
    rm seds_100614.tar.gz
}
