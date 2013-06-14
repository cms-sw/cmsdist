### RPM external gridsite 1.0.0
%define gridsite_major_version 1
%define gridsite_minor_version 0
%define gridsite_micro_version 0
%define gridsite_version %gridsite_major_version.%gridsite_minor_version.%gridsite_micro_version
## INITENV CMD ln -sf $GRIDSITE_ROOT/lib/mod_gridsite.so $APACHE_ROOT/modules
## INITENV CMD ln -sf $GRIDSITE_ROOT/etc/gridsite.conf $APACHE_ROOT/conf.d
## INITENV +PATH LD_LIBRARY_PATH %i/lib


Source: http://www.gridsite.org/download/old-releases/%{n}-%{v}.src.tar.gz
Patch0: gridsite-makefiles
Patch1: gridsite-flag
Patch2: gridsite-purpose
Patch3: gridsite-grst

Requires: libxml2 apache

%description
GridSite adds GSI, VOMS and GACL support to Apache 2.0 (mod_gridsite),
a library for manipulating these technologies (libgridsite), and CGI
programs for interactive management of HTTP(S) servers (gridsite-admin.cgi)

See http://www.gridpp.ac.uk/gridsite/ for details.

%prep

%setup -n %n-%v
%patch0 -p0
%patch1 -p0
%patch2 -p0
%patch3 -p0

%build
cd lib
export CFLAGS="-I$OPENSSL_ROOT/include/openssl"
export LDFLAGS="-I$OPENSSL_ROOT/lib"
make MYCFLAGS="-I$OPENSSL_ROOT/include -I$OPENSSL_ROOT/include/openssl -I$APACHE_ROOT/include -DOPENSSL_NO_KRB5" prefix=%i install_prefix=%i
cd ../mod
make MYCFLAGS="-I$OPENSSL_ROOT/include -I$OPENSSL_ROOT/include/openssl -I$APACHE_ROOT/include -DOPENSSL_NO_KRB5" prefix=%i install_prefix=%i

%install

# Install libraries
cd lib
mkdir -p %i/include \
         %i/lib \
         %i/bin \
         %i/share/doc/gridsite-%{gridsite_version}
cp -f gridsite.h %i/include
cp -f gridsite-gacl.h %i/include
cp -f libgridsite.a %i/lib
cp -f  libgridsite.so.%{gridsite_version} %i/lib

BDIR=`pwd`
cd %i/lib
ln -sf libgridsite.so.%{gridsite_version} \
                         libgridsite.so
ln -sf libgridsite.so.%{gridsite_version} \
                         libgridsite.so.%{gridsite_major_version}
ln -sf libgridsite.so.%{gridsite_version} \
                         libgridsite.so.%{gridsite_major_version}.%{gridsite_minor_version}
cd $BDIR

# Install modules
cd ../mod
cp -f mod_gridsite.so %i/lib
cd ..

# Install config
mkdir -p %i/etc
echo -e "LoadModule gridsite_module %i/lib/mod_gridsite.so" > \
     %i/etc/gridsite.conf

