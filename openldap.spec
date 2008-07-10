### RPM external openldap 2.3.39
Source: ftp://ftp.openldap.org/pub/OpenLDAP/openldap-stable/openldap-stable-20071118.tgz
Requires: openssl db4
Provides: libsasl2.so.2

#http://www.openssl.org/source/%n-%realversion.tar.gz

%prep
%setup -q -n %n-%{realversion}
pwd
%build

#  CC          C compiler command
#  CFLAGS      C compiler flags
#  LDFLAGS     linker flags, e.g. -L<lib dir> if you have libraries in a
#              nonstandard directory <lib dir>
#  CPPFLAGS    C/C++ preprocessor flags, e.g. -I<include dir> if you have
#              headers in a nonstandard directory <include dir>
#  CPP         C preprocessor

%define gcc_setup CC=$GCC_ROOT/bin/cc
%define ssl_setup CPPFLAGS=-I$OPENSSL_ROOT/include LDFLAGS=-L$OPENSSL_ROOT/lib
%define db4_setup CPPFLAGS=-I$DB4_ROOT/include LDFLAGS=-L$DB4_ROOT/lib

%gcc_setup %ssl_setup %db4_setup ./configure --prefix=%i --with-cyrus-sasl --with-tls
make depend
make
%install
make install
