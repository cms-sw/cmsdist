### RPM external openssl 0.9.7d-CMS3
Source: http://www.openssl.org/source/%n-%realversion.tar.gz

%prep
%setup -n %n-%{realversion}

%build
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
