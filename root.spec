### RPM lcg root 5.18.00-lite
## INITENV +PATH PYTHONPATH %i/lib/python
## INITENV SET ROOTSYS %i

Source: ftp://root.cern.ch/%n/%{n}_v%{realversion}.source.tar.gz

#Requires: gccxml python qt gsl castor openssl mysql libpng libjpg dcap pcre zlib oracle libungif
Requires: gccxml python qt gsl libjpg libpng dcap pcre libtiff libungif zlib

%prep
%setup -n root

%build
mkdir -p %i
export ROOTSYS=%_builddir/root
CONFIG_ARGS="--enable-table 
             --disable-builtin-pcre
             --disable-builtin-freetype
             --disable-builtin-zlib
             --disable-oracle
             --disable-mysql
             --disable-qtgsi
             --disable-qt
             --disable-rfio
             --disable-castor
             --disable-ldap
             --disable-krb5
             --disable-pgsql
             --disable-xml
             --enable-python --with-python-libdir=${PYTHON_ROOT}/lib --with-python-incdir=${PYTHON_ROOT}/include/python2.4 
             --enable-explicitlink 
             --enable-mathcore 
             --enable-mathmore
             --enable-reflex  
             --enable-cintex 
             --enable-minuit2 
             --enable-roofit
             --with-gccxml=${GCCXML_ROOT} 
             --with-ssl-incdir=${OPENSSL_ROOT}/include
             --with-ssl-libdir=${OPENSSL_ROOT}/lib
             --with-gsl-incdir=${GSL_ROOT}/include
             --with-gsl-libdir=${GSL_ROOT}/lib
             --with-dcap-libdir=${DCAP_ROOT}/lib 
             --with-dcap-incdir=${DCAP_ROOT}/include"

case $(uname)-$(uname -p) in
  Linux-x86_64)
    ./configure linuxx8664gcc $CONFIG_ARGS --disable-astiff --disable-cern;; 
  Linux-i*86)
    ./configure linux  $CONFIG_ARGS;;
  Darwin*)
    ./configure macosx $CONFIG_ARGS;;
  Linux-ppc64*)
    ./configure linux $CONFIG_ARGS;;
esac

make  %makeprocesses
make cintdlls
%install
# Override installers if we are using GNU fileutils cp.  On OS X
# ROOT's INSTALL is defined to "cp -pPR", which only works with
# the system cp (/bin/cp).  If you have fileutils on fink, you
# lose.  Check which one is getting picked up and select syntax
# accordingly.  (FIXME: do we need to check that -P is accepted?)
if (cp --help | grep -e '-P.*--parents') >/dev/null 2>&1; then
  cp="cp -dpR"
else
  cp="cp -pPR"
fi

export ROOTSYS=%i
make INSTALL="$cp" INSTALLDATA="$cp" install
mkdir -p $ROOTSYS/lib/python
cp -r reflex/python/genreflex $ROOTSYS/lib/python
#
