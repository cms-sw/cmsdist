### RPM external nmap 6.49BETA4
## INITENV +PATH PYTHONPATH %i/${PYTHON_LIB_SITE_PACKAGES}
Source: https://nmap.org/dist/%n-%realversion.tar.bz2
Requires: pcre

%prep
%setup -n %n-%{realversion}

%build
./configure --prefix=%{i} --enable-static=no --without-zenmap
make %makeprocesses

%install
make install
perl -p -i -e 's{^#!.*/python2}{#!/usr/bin/env python}' %i/bin/ndiff
