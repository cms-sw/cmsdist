### RPM external distcc 3.2rc1
Source: https://distcc.googlecode.com/files/distcc-%realversion.tar.gz
Requires: python

%prep
%setup -n %n-%realversion
%build
./configure --prefix %i  --without-gtk --without-gnome CFLAGS="-O2 -Wno-unused-but-set-variable" CC="`which gcc`" PYTHON=$PYTHON_ROOT/bin/python
make %makeprocesses
%install
make install
