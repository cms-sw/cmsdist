### RPM external thepeg 1.6.1
## BUILDIF case $(uname):$(uname -m) in Linux:i*86 ) true ;; Linux:x86_64 ) true ;;  Linux:ppc64 ) false ;; Darwin:* ) false ;; * ) false ;; esac

#Source: http://www.thep.lu.se/~leif/ThePEG/ThePEG-%{realversion}.tgz
#Source: http://projects.hepforge.org/herwig/files/ThePEG-%{realversion}.tar.gz
Source: http://service-spi.web.cern.ch/service-spi/external/MCGenerators/distribution/thepeg-%{realversion}-src.tgz
Patch0: thepeg-1.6.1-break-termcap-dependence
Patch1: thepeg-1.6.1-units
Requires: lhapdf
Requires: gsl

%prep
%setup -q -n %{n}/%{realversion}
%patch0 -p2
%patch1 -p2

%build
./configure --with-LHAPDF=$LHAPDF_ROOT/lib --without-javagui --prefix=%i --with-gsl=$GSL_ROOT --disable-readline
make

%install

make install
rm %i/share/ThePEG/Doc/fixinterfaces.pl

%post
%{relocateConfig}lib/ThePEG/*.la

