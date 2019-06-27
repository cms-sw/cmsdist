### RPM external ccache 3.1.8
Source: http://samba.org/ftp/ccache/ccache-%realversion.tar.bz2

%prep
%setup -n %n-%realversion
./configure --prefix %i
make %makeprocesses
%install
make install
ln -sf ccache %i/bin/cc
ln -sf ccache %i/bin/gcc
ln -sf ccache %i/bin/c++
ln -sf ccache %i/bin/g++
ln -sf ccache %i/bin/gfortran
# bla bla
