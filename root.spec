### RPM lcg root 5.10.00
# Source: cvs://:pserver:cvs@root.cern.ch:2401/user/cvs?passwd=Ah<Z&tag=-rv%(echo %v | tr . -)&module=root&output=/%{n}_v%{v}.source.tar.gz
Source: ftp://root.cern.ch/%n/%{n}_v%{v}.source.tar.gz
Requires: gccxml python qt gsl
%prep
%setup -n root

%build
mkdir -p %i
export ROOTSYS=%i
CONFIG_ARGS="--enable-table 
             --with-gccxml=${GCCXML_ROOT} 
             --enable-python --with-python-libdir=${PYTHON_ROOT}/lib --with-python-incdir=${PYTHON_ROOT}/include 
             --enable-explicitlink 
             --enable-qt --with-qt-libdir=${QT_ROOT}/lib --with-qt-incdir=${QT_ROOT}/include 
             --enable-mathcore 
             --enable-reflex  
             --enable-cintex 
             --enable-minuit2 
             --enable-roofit"

case $(uname)-$(uname -m) in
  Linux-x86_64)
    ./configure linuxx8664gcc $CONFIG_ARGS;; 
  Linux*)
    ./configure linux $CONFIG_ARGS;;
  Darwin)
    ./configure macosx $CONFIG_ARGS;;
esac

make %makeprocesses

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
