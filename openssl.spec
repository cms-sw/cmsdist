### RPM external openssl 0.9.7d
Requires: gcc-wrapper
Source: http://www.openssl.org/source/%n-%v.tar.gz

%build
## IMPORT gcc-wrapper
./config --prefix=%i shared
case $(uname)-$(uname -m) in
  Darwin*)
    perl -p -i -e 's|-compatibility_version.*|-compatibility_version \${SHLIB_MAJOR}.\${SHLIB_MINOR} \\|' Makefile.ssl
esac

make
%install
make install
perl -p -i -e "s|^#!.*perl|#!/usr/bin/env perl|" %{i}/ssl/misc/CA.pl %{i}/ssl/misc/der_chop %{i}/bin/c_rehash
#
