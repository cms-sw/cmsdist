### RPM external ccache 2.4
## INITENV SET CCACHE_DIR %_builddir/.ccache
## INITENV CMD ccache -M 1G
## INITENV +PATH PATH $GCC_ROOT/bin
Source: http://ccache.samba.org/ftp/%n/%n-%v.tar.gz

%install
make install
ln -sf ccache %i/bin/cc
ln -sf ccache %i/bin/gcc
ln -sf ccache %i/bin/c++
ln -sf ccache %i/bin/g++
