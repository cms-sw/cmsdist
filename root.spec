### RPM lcg root 5.14.00f-CMS2
## INITENV +PATH PYTHONPATH %i/lib/python
## INITENV SET ROOTSYS %i
Source: cvs://:pserver:cvs@root.cern.ch:2401/user/cvs?passwd=Ah<Z&tag=-rv%(echo %realversion | tr . -)&module=root&output=/%{n}_v%{realversion}.source.tar.gz
#Source: ftp://root.cern.ch/%n/%{n}_v%{realversion}.source.tar.gz

Patch: root-CINT-maxlongline
Patch1: root_libpng

%define cpu %(echo %cmsplatf | cut -d_ -f2)
%define pythonv %(echo $PYTHON_VERSION | cut -d. -f1,2)
Requires: gccxml python qt gsl castor openssl mysql libpng libjpg dcap pcre zlib oracle libungif

%if "%cpu" != "amd64"
Requires: libtiff
%endif

%prep
%setup -n root
%patch -p0
%patch1 -p2

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
             --with-ssl-incdir=${OPENSSL_ROOT}/include
             --with-ssl-libdir=${OPENSSL_ROOT}/lib
             --with-gsl-incdir=${GSL_ROOT}/include
             --with-gsl-libdir=${GSL_ROOT}/lib
             --with-dcap-libdir=${DCAP_ROOT}/lib 
             --with-dcap-incdir=${DCAP_ROOT}/include
             --disable-pgsql
             --disable-xml"

case $(uname)-$(uname -p) in
  Linux-x86_64)
    ./configure linuxx8664gcc $CONFIG_ARGS --enable-oracle --with-oracle-libdir=${ORACLE_ROOT}/lib --with-oracle-incdir=${ORACLE_ROOT}/include --with-shift-libdir=${CASTOR_ROOT}/lib --with-shift-incdir=${CASTOR_ROOT}/include/shift --disable-astiff --disable-cern;; 
  Linux-i*86)
    ./configure linux  $CONFIG_ARGS --enable-oracle --with-oracle-libdir=${ORACLE_ROOT}/lib --with-oracle-incdir=${ORACLE_ROOT}/include --with-shift-libdir=${CASTOR_ROOT}/lib --with-shift-incdir=${CASTOR_ROOT}/include/shift;;
  Darwin*)
    ./configure macosx $CONFIG_ARGS --disable-rfio;;
  Linux-ppc64*)
    ./configure linux $CONFIG_ARGS --disable-rfio;;
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
