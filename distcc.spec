### RPM external distcc 3.2rc1
Source: https://distcc.googlecode.com/files/distcc-%realversion.tar.gz
Requires: python

%prep
%setup -n %n-%realversion
%build
CFLAGS="-O2 -Wno-unused-but-set-variable -Wno-unused-local-typedefs -Wno-unused-parameter"
./configure --prefix %i  --without-gtk --without-gnome CFLAGS="$CFLAGS" CC="`which gcc`" PYTHON=$PYTHON_ROOT/bin/python
make %makeprocesses
%install
make install
ln -sf distcc %i/bin/c++
ln -sf distcc %i/bin/cc
ln -sf distcc %i/bin/gcc
ln -sf distcc %i/bin/gfortran
%post
%{relocateConfig}bin/pump
