### RPM external openssl 0.9.7d
Source: http://www.openssl.org/source/%n-%v.tar.gz
Requires: perl

%build
./config --prefix=%i shared
make
%install
make install
perl -p -i -e "s|^#!.*perl|#!/usr/bin/env perl|" %{i}/ssl/misc/CA.pl %{i}/ssl/misc/der_chop %{i}/bin/c_rehash
