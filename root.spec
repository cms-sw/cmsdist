### RPM lcg root 5.08.00
# Source: cvs://:pserver:cvs@root.cern.ch:2401/user/cvs?passwd=Ah<Z&tag=-rv%(echo %v | tr . -)&module=root&output=/%{n}_v%{v}.source.tar.gz
Source: ftp://root.cern.ch/%n/%{n}_v%{v}.source.tar.gz

%prep
%setup -n root

%build
mkdir -p %i
export ROOTSYS=%i
case $(uname) in
  Linux)
    ./configure linux ;;
  Darwin)
    ./configure macosx ;;
esac
make

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
