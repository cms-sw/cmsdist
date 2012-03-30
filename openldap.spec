### RPM external openldap 2.3.39
## INITENV +PATH LD_LIBRARY_PATH %i/lib
Source: ftp://ftp.openldap.org/pub/OpenLDAP/openldap-stable/openldap-stable-20071118.tgz
Patch0: openldap-2.3.39-gcc44
Patch1: openldap-2.3.39-gcc46
Requires: openssl db4 

%define isslc6 %(case %cmsplatf in (slc6*) echo true ;; (*) echo false ;; esac)

%if "%isslc6" == "true"
# On SLC6 we build missing Cyrus SASL.
Requires: cyrus-sasl
%else
Provides: libsasl2.so.2 libsasl2.so.2()(64bit)
%endif

%prep
%setup -q -n %n-%{realversion}
%patch0 -p1
%patch1 -p1

%build

#  CC          C compiler command
#  CFLAGS      C compiler flags
#  LDFLAGS     linker flags, e.g. -L<lib dir> if you have libraries in a
#              nonstandard directory <lib dir>
#  CPPFLAGS    C/C++ preprocessor flags, e.g. -I<include dir> if you have
#              headers in a nonstandard directory <include dir>
#  CPP         C preprocessor

CYRUS_SASL_ROOT=${CYRUS_SASL_ROOT:-"/usr"}
export CPPFLAGS="-D_GNU_SOURCE -I$OPENSSL_ROOT/include -I$DB4_ROOT/include -I$CYRUS_SASL_ROOT/include"
export LDFLAGS="-L$OPENSSL_ROOT/lib -L$DB4_ROOT/lib -L$CYRUS_SASL_ROOT/lib -L%{_builddir}/%n-%{realversion}/sasl2lib"

./configure --prefix=%i --with-cyrus-sasl --with-tls --disable-static
make depend
make
%install
make install
# Read documentation online.
rm -rf %i/man
