### RPM lcg root 5.12.00-forCMS139
# INITENV +PATH PYTHONPATH %i/lib/python
%define realVersion %(echo %v | cut -d- -f1)
Source: cvs://:pserver:cvs@root.cern.ch:2401/user/cvs?passwd=Ah<Z&tag=-rv%(echo %realVersion | tr . -)&module=root&output=/%{n}_v%{realVersion}.source.tar.gz
#Source: ftp://root.cern.ch/%n/%{n}_v%{realVersion}.source.tar.gz
%define cpu %(echo %cmsplatf | cut -d_ -f2)
%define pythonv %(echo $PYTHON_VERSION | cut -d. -f1,2)
Requires: gccxml python qt gsl castor openssl mysql libpng libjpg dcap pcre zlib oracle

%if "%cpu" != "amd64"
Requires: libtiff
%endif

Patch: root-cint-bug
%prep
%setup -n root
%build
mkdir -p %i
export ROOTSYS=%_builddir/root
CONFIG_ARGS="--enable-table 
             --disable-builtin-pcre
             --disable-builtin-freetype
             --disable-builtin-zlib
             --with-gccxml=${GCCXML_ROOT} 
             --enable-python --with-python-libdir=${PYTHON_ROOT}/lib --with-python-incdir=${PYTHON_ROOT}/include/python2.4 
             --enable-mysql --with-mysql-libdir=${MYSQL_ROOT}/lib --with-mysql-incdir=${MYSQL_ROOT}/include
             --enable-oracle --with-oracle-libdir=${ORACLE_ROOT}/lib --with-oracle-incdir=${ORACLE_ROOT}/include
             --enable-explicitlink 
             --enable-qtgsi
             --enable-qt --with-qt-libdir=${QT_ROOT}/lib --with-qt-incdir=${QT_ROOT}/include 
             --enable-mathcore 
             --enable-mathmore
             --enable-reflex  
             --enable-cintex 
             --enable-minuit2 
             --enable-roofit
             --disable-ldap
             --disable-krb5
	         --with-dcap-libdir=${DCAP_ROOT}/lib 
             --with-dcap-incdir=${DCAP_ROOT}/include
             --with-ssl-incdir=${OPENSSL_ROOT}/include
             --with-ssl-libdir=${OPENSSL_ROOT}/lib
             --with-shift-incdir=${CASTOR_ROOT}/include/shift
             --with-shift-libdir=${CASTOR_ROOT}/lib
             --disable-pgsql
             --disable-xml"

case $(uname)-$(uname -m) in
  Linux-x86_64)
    ./configure linuxx8664gcc $CONFIG_ARGS --disable-astiff;; 
  Linux*)
    ./configure linux $CONFIG_ARGS;;
  Darwin*)
    ./configure macosx $CONFIG_ARGS;;
esac

make 
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

export ROOTSYS=%i/root
make INSTALL="$cp" INSTALLDATA="$cp" install
mkdir -p %i/root/lib/python
cp -r reflex/python/genreflex %i/root/lib/python
#
