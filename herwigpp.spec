### RPM external herwigpp 7.0.1
Source: https://www.hepforge.org/archive/herwig/Herwig-%{realversion}.tar.bz2

# Needed later during make / make install
Source1: https://www.hepforge.org/archive/lhapdf/pdfsets/6.1/MMHT2014lo68cl.tar.gz
Source2: https://www.hepforge.org/archive/lhapdf/pdfsets/6.1/MMHT2014nlo68cl.tar.gz


Requires: lhapdf
Requires: boost 
Requires: thepeg
Requires: gsl 
Requires: hepmc
Requires: fastjet
Requires: madgraph5amcatnlo
Requires: openloops

Patch0: herwigpp-missingBoostMTLib

BuildRequires: autotools
BuildRequires: lhapdf


%if "%{?cms_cxx:set}" != "set"
%define cms_cxx g++
%endif


%prep
%setup -q -n Herwig-%{realversion}

%patch0 -p1 

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
            --with-openloops=$OPENLOOPS_ROOT \
            --prefix=%i \
            CXX="$CXX" CC="$CC" \
	    BOOST_ROOT="$BOOST_ROOT" LDFLAGS="$LDFLAGS -L$BOOST_ROOT/lib" \
            LHAPDF_DATA_PATH="$LHAPDF_ROOT/share/LHAPDF"


# Extract needed PDFs since PDFs on cvmfs are not available during build
tar xvfz %{_sourcedir}/MMHT2014lo68cl.tar.gz
tar xvfz %{_sourcedir}/MMHT2014nlo68cl.tar.gz
# Export LHAPDF_DATA_PATH since it is needed during make
LHAPDF_DATA_PATH=%{_sourcedir}:$LHAPDF_DATA_PATH:$LHAPDF_ROOT/share/LHAPDF

make %makeprocesses

%install
make install

# Remove downloaded PDFs required during make
rm -rf %{_sourcedir}/MMHT2014*

%post
%{relocateConfig}share/Herwig7/HerwigDefaults.rpo
