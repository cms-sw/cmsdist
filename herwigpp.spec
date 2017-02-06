### RPM external herwigpp 7.0.1
Source: https://www.hepforge.org/archive/herwig/Herwig-%{realversion}.tar.bz2
Requires: boost 
Requires: thepeg
Requires: gsl 
Requires: hepmc
Requires: fastjet
Requires: gengetopt
Requires: madgraph5amcatnlo
Requires: openloops
Requires: lhapdf

Patch0: herwigpp-missingBoostMTLib
Patch1: herwigpp-mainMakefileam
Patch2: herwigpp-srcMakefileam

BuildRequires: autotools
BuildRequires: gengetopt
BuildRequires: lhapdf

%if "%{?cms_cxx:set}" != "set"
%define cms_cxx g++
%endif

%if "%{?cms_cxxflags:set}" != "set"
%define cms_cxxflags -O2 -std=c++14
%endif

%prep
%setup -q -n Herwig-%{realversion}

%patch0 -p1 
%patch1 -p1
%patch2 -p1

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
