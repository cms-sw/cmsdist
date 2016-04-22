### RPM external thepeg 2.0.1
## INITENV +PATH LD_LIBRARY_PATH %{i}/lib/ThePEG
## INITENV +PATH DYLD_LIBRARY_PATH %{i}/lib/ThePEG

# Download from official webpage
Source: http://www.hepforge.org/archive/thepeg/ThePEG-%{realversion}.tar.gz

Requires: lhapdf
Requires: gsl
Requires: hepmc
Requires: zlib
Requires: fastjet
Requires: rivet


BuildRequires: autotools

%define keep_archives true

%if "%{?cms_cxx:set}" != "set"
%define cms_cxx c++
%endif


%prep
%setup -q -n ThePEG-%{realversion}

# Regenerate build scripts
autoreconf -fiv

%build
CXX="$(which %{cms_cxx}) -fPIC"
CC="$(which gcc) -fPIC"
PLATF_CONF_OPTS="--enable-shared --disable-static"


./configure $PLATF_CONF_OPTS \
            --with-lhapdf=$LHAPDF_ROOT \
            --with-boost=$BOOST_ROOT \
            --with-hepmc=$HEPMC_ROOT \
            --with-gsl=$GSL_ROOT \
            --with-zlib=$ZLIB_ROOT \
            --with-fastjet=$FASTJET_ROOT \
            --with-rivet=$RIVET_ROOT \
            --without-javagui \
            --prefix=%{i} \
            --disable-readline CXX="$CXX" CC="$CC"  

make %{makeprocesses}

%install
make install
find %{i}/lib -name '*.la' -exec rm -f {} \;

%post
%{relocateConfig}lib/ThePEG/Makefile.common
%{relocateConfig}lib/ThePEG/Makefile
%{relocateConfig}lib/ThePEG/ThePEGDefaults.rpo
%{relocateConfig}lib/ThePEG/ThePEGDefaults-%{realversion}.rpo
