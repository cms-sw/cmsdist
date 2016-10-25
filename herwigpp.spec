### RPM external herwigpp 7.0.2
Source: https://www.hepforge.org/archive/herwig/Herwig-%{realversion}.tar.bz2
#Source: https://mharrend.web.cern.ch/mharrend/herwig7/Herwig-7.0.2.tar.bz2

# Tried to comment out the parts which build HerwigDefaults.rpo during make install

%define isamd64 %(case %{cmsplatf} in (*amd64*) echo 1 ;; (*) echo 0 ;; esac)

Requires: lhapdf
Requires: boost 
Requires: thepeg
Requires: gsl 
Requires: hepmc
Requires: fastjet
Requires: madgraph5amcatnlo

%if %isamd64
Requires: openloops
%endif

# Patch since otherwise Boost wants multithreaded lib, even though only single-threaded lib is installed
# Problem exists since Herwig++3Beta

Patch0: herwigpp-missingBoostMTLib


BuildRequires: autotools


%if "%{?cms_cxx:set}" != "set"
%define cms_cxx g++
%endif


%prep
%setup -q -n Herwig-%{realversion}

%patch0 -p1 
# %patch1 -p1

# Regenerate build scripts
autoreconf -fiv

%build
CXX="$(which %{cms_cxx}) -fPIC"
CC="$(which gcc) -fPIC"
PLATF_CONF_OPTS="--enable-shared --disable-static"

./configure $PLATF_CONF_OPTS \
            --with-thepeg=$THEPEG_ROOT \
            --with-fastjet=$FASTJET_ROOT \
            --with-gsl=$GSL_ROOT \
            --with-boost=$BOOST_ROOT \
	    --with-madgraph=$MADGRAPH5AMCATNLO_ROOT \
%if %isamd64
            --with-openloops=$OPENLOOPS_ROOT \
%endif
            --prefix=%i \
            CXX="$CXX" CC="$CC" \
	    BOOST_ROOT="$BOOST_ROOT" LDFLAGS="$LDFLAGS -L$BOOST_ROOT/lib" \
            LD_LIBRARY_PATH=$LHAPDF_ROOT/lib:$GSL_ROOT/lib:$LD_LIBRARY_PATH
            


make %makeprocesses all LD_LIBRARY_PATH=$LHAPDF_ROOT/lib:$THEPEG_ROOT/lib/ThePEG:$GSL_ROOT/lib:$FASTJET_ROOT/lib:$BOOST_ROOT/lib:$LD_LIBRARY_PATH LIBRARY_PATH=$FASTJET_ROOT/lib

%install
make install LD_LIBRARY_PATH=$LHAPDF_ROOT/lib:$THEPEG_ROOT/lib/ThePEG:$GSL_ROOT/lib:$FASTJET_ROOT/lib:$BOOST_ROOT/lib:$LD_LIBRARY_PATH LIBRARY_PATH=$FASTJET_ROOT/lib:$THEPEG_ROOT/lib/ThePEG:$LHAPDF_ROOT/lib LHAPDF_DATA_PATH=$LHAPDF_ROOT/share/LHAPDF



%post
%{relocateConfig}share/Herwig/HerwigDefaults.rpo
