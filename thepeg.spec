### RPM external thepeg 1.6.1
## INITENV +PATH LD_LIBRARY_PATH %i/lib/ThePEG
## INITENV +PATH DYLD_LIBRARY_PATH %i/lib/ThePEG
#Source: http://www.thep.lu.se/~leif/ThePEG/ThePEG-%{realversion}.tgz
#Source: http://projects.hepforge.org/herwig/files/ThePEG-%{realversion}.tar.gz
Source: http://service-spi.web.cern.ch/service-spi/external/MCGenerators/distribution/thepeg-%{realversion}-src.tgz
Patch0: thepeg-1.6.1-break-termcap-dependence
Patch1: thepeg-1.6.1-units
Patch2: thepeg-1.6.1-use-dylibs-macosx
Requires: lhapdf
Requires: gsl
# FIXME: hepmc?
# FIXME: rivet?
%if "%(echo %cmsos | grep osx >/dev/null && echo true)" == "true"
Requires: gfortran-macosx
%endif

%prep
%setup -q -n %{n}/%{realversion}
%patch0 -p2
%patch1 -p2
%if "%(echo %cmsos | grep osx >/dev/null && echo true)" == "true"
%patch2 -p1
%endif

%build
./configure --with-LHAPDF=$LHAPDF_ROOT/lib --without-javagui --prefix=%i --with-gsl=$GSL_ROOT --disable-readline
make

%install

make install
rm %i/share/ThePEG/Doc/fixinterfaces.pl

%post
%{relocateConfig}lib/ThePEG/*.la
