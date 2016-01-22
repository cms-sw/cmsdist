### RPM external herwigpp 7.0.0
Source: https://www.hepforge.org/archive/herwig/Herwig-7.0.0.tar.bz2
Requires: boost 
Requires: thepeg
Requires: gsl 
Requires: hepmc
Requires: fastjet
Requires: gengetopt
Requires: madgraph5amcatnlo
Requires: openloops

Patch0: herwigpp-missingBoostMTLib

BuildRequires: autotools

%if "%{?cms_cxx:set}" != "set"
%define cms_cxx g++
%endif

%if "%{?cms_cxxflags:set}" != "set"
%define cms_cxxflags -O2 -std=c++11
%endif

%prep
%setup -q -n Herwig-7.0.0

%patch0 -p1 

# Regenerate build scripts
autoreconf -fiv

%build
CXX="$(which %{cms_cxx}) -fPIC"
CC="$(which gcc) -fPIC"
PLATF_CONF_OPTS="--enable-shared --disable-static"


./configure $PLATF_CONF_OPTS \
            --disable-silent-rules \
            --with-thepeg=$THEPEG_ROOT \
            --with-fastjet=$FASTJET_ROOT \
            --with-gsl=$GSL_ROOT \
            --with-boost=$BOOST_ROOT \
            --with-madgraph=$MADGRAPH5AMCATNLO_ROOT \
            --with-openloops=$OPENLOOPS_ROOT \
            --prefix=%i \
            CXX="$CXX" CC="$CC" CXXFLAGS="%{cms_cxxflags}" \
	    BOOST_ROOT="$BOOST_ROOT" LDFLAGS="$LDFLAGS -L$BOOST_ROOT/lib"

make %makeprocesses

%install
#tar -c -h lib include | tar -x -C %i
make install

%post
%{relocateConfig}share/Herwig7/HerwigDefaults.rpo
