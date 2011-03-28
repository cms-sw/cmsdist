### RPM external thepeg 1.6.1
## INITENV +PATH LD_LIBRARY_PATH %i/lib/ThePEG
## INITENV +PATH DYLD_LIBRARY_PATH %i/lib/ThePEG
#Source: http://www.thep.lu.se/~leif/ThePEG/ThePEG-%{realversion}.tgz
#Source: http://projects.hepforge.org/herwig/files/ThePEG-%{realversion}.tar.gz
Source: http://service-spi.web.cern.ch/service-spi/external/MCGenerators/distribution/thepeg-%{realversion}-src.tgz
Patch0: thepeg-1.6.1-break-termcap-dependence
Patch1: thepeg-1.6.1-units
Patch2: thepeg-1.6.1-use-dylibs-macosx
Patch3: thepeg-1.6.1-lhapdf-env
Patch4: thepeg-1.6.1-gcc46
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
%patch3 -p2
%patch4 -p2

%build
# configure does not handle linking against archive LHAPDF
# notice that we should probably build an archive library
# also for this library, but we do not care for the moment.
perl -p -i -e 's|LHAPDF[.]dylib|LHAPDF.a|' configure
FC=`which gfortran`
./configure --enable-shared --disable-static \
            --with-LHAPDF=$LHAPDF_ROOT/lib \
            --without-javagui --prefix=%i --with-gsl=$GSL_ROOT \
            --disable-readline \
            FC=$FC \
            LIBS="`$FC --print-file-name=libgfortranbegin.a` `$FC --print-file-name=libgfortran.a`"
make

%install

make install
rm %i/share/ThePEG/Doc/fixinterfaces.pl

%post
%{relocateConfig}lib/ThePEG/*.la
