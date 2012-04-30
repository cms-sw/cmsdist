### RPM external hepmc 2.06.07
Source: http://lcgapp.cern.ch/project/simu/HepMC/download/HepMC-%realversion.tar.gz
Patch0: hepmc-2.03.06-reflex

%define keep_archives true
%if "%(case %cmsplatf in (osx*_*_gcc421) echo true ;; (*) echo false ;; esac)" == "true"
Requires: gfortran-macosx
%endif

%if "%{?cms_cxx:set}" != "set"
%define cms_cxx c++
%endif

%if "%{?cms_cxxflags:set}" != "set"
%define cms_cxxflags -std=c++0x
%endif

%prep
%setup -q -n HepMC-%{realversion}
%patch0 -p0

case %cmsplatf in
  slc5_*_gcc4[01234]*) 
    F77="`which gfortran`"
    CXX="`which %cms_cxx`"
    PLATF_CONFIG_OPTS=""
  ;;
  *)
    F77="`which gfortran` -fPIC"
    CXX="`which %cms_cxx` -fPIC"
    PLATF_CONFIG_OPTS="--enable-static --disable-shared"
  ;;
esac
./bootstrap
./configure $PLATF_CONFIG_OPTS --prefix=%{i} --with-momentum=GEV --with-length=MM F77="$F77" CXX="$CXX" CXXFLAGS="%cms_cxxflags"

%build
make %makeprocesses

%install
make install
rm -rf %i/lib/*.la
