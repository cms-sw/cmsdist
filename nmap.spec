### RPM external nmap 6.49BETA4
## INITENV +PATH PYTHONPATH %i/${PYTHON_LIB_SITE_PACKAGES}
Source: https://nmap.org/dist/%n-%realversion.tar.bz2
Requires: openssl

%prep
%setup -n %n-%{realversion}

%build
./configure --prefix=%{i} --enable-static=no --without-zenmap --with-openssl=$OPENSSL_ROOT
make %makeprocesses

%install
make install
