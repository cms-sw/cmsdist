### RPM external thepeg 1.7.0
## INITENV +PATH LD_LIBRARY_PATH %i/lib/ThePEG
## INITENV +PATH DYLD_LIBRARY_PATH %i/lib/ThePEG
#Source: http://www.thep.lu.se/~leif/ThePEG/ThePEG-%{realversion}.tgz
#Source: http://projects.hepforge.org/herwig/files/ThePEG-%{realversion}.tar.gz
Source: http://service-spi.web.cern.ch/service-spi/external/MCGenerators/distribution/thepeg-%{realversion}-src.tgz
Patch0: thepeg-1.7.0-break-termcap-dependence
Patch1: thepeg-1.7.0-use-dylibs-macosx
Patch2: thepeg-1.6.1-lhapdf-env
Patch3: thepeg-1.6.1-gcc46
Requires: lhapdf
Requires: gsl
Requires: hepmc
# FIXME: rivet?
%if "%(echo %cmsos | grep osx >/dev/null && echo true)" == "true"
Requires: gfortran-macosx
%endif

%prep
%setup -q -n %{n}/%{realversion}
%patch0 -p2
%if "%(echo %cmsos | grep osx >/dev/null && echo true)" == "true"
%patch1 -p1
%endif
%patch2 -p2
%patch3 -p2

%build
./configure --with-LHAPDF=$LHAPDF_ROOT/lib --with-hepmc=$HEPMC_ROOT --with-gsl=$GSL_ROOT --without-javagui --prefix=%i --disable-readline
make

%install

make install
rm %i/share/ThePEG/Doc/fixinterfaces.pl

%post
%{relocateConfig}lib/ThePEG/*.la
