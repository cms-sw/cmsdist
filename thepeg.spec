### RPM external thepeg 2.1.4
## INITENV +PATH LD_LIBRARY_PATH %{i}/lib/ThePEG
## INITENV +PATH DYLD_LIBRARY_PATH %{i}/lib/ThePEG

# Download from official webpage
Source: http://www.hepforge.org/archive/thepeg/ThePEG-%{realversion}.tar.bz2
Patch0: thepeg-2.1.1-gcc8

Requires: lhapdf
Requires: gsl OpenBLAS
Requires: hepmc
Requires: zlib
Requires: fastjet
Requires: rivet
BuildRequires: autotools
BuildRequires: lhapdf

%define keep_archives true

%if "%{?cms_cxx:set}" != "set"
%define cms_cxx c++
%endif


%prep
%setup -q -n ThePEG-%{realversion}
%patch0 -p1
# Regenerate build scripts
autoreconf -fiv

%build
CXX="$(which %{cms_cxx}) -fPIC"
CC="$(which gcc) -fPIC"
PLATF_CONF_OPTS="--enable-shared --disable-static"


# Update to detect aarch64 and ppc64le
rm -f ./Config/config.{sub,guess}
curl -L -k -s -o ./Config/config.guess http://cmsrep.cern.ch/cmssw/download/config/config.guess
curl -L -k -s -o ./Config/config.sub http://cmsrep.cern.ch/cmssw/download/config/config.sub
chmod +x ./Config/config.{sub,guess}

sed -i -e "s|-lgslcblas|-lopenblas|" ./configure
./configure $PLATF_CONF_OPTS \
            --with-lhapdf=$LHAPDF_ROOT \
            --with-boost=$BOOST_ROOT \
            --with-hepmc=$HEPMC_ROOT \
            --with-gsl=$GSL_ROOT \
            --with-zlib=$ZLIB_ROOT \
            --with-fastjet=$FASTJET_ROOT \
            --without-javagui \
            --prefix=%{i} \
            --disable-readline CXX="$CXX" CC="$CC" LDFLAGS="-L${OPENBLAS_ROOT}/lib"

make %{makeprocesses}

%install
make install
find %{i}/lib -name '*.la' -exec rm -f {} \;


%post
%{relocateConfig}lib/ThePEG/Makefile.common
%{relocateConfig}lib/ThePEG/Makefile
%{relocateConfig}lib/ThePEG/ThePEGDefaults.rpo
%{relocateConfig}lib/ThePEG/ThePEGDefaults-%{realversion}.rpo

#create link to LesHouches library

cd $RPM_INSTALL_PREFIX/%{pkgrel}/lib/ThePEG/
ln -s LesHouches.so libLesHouches.so
