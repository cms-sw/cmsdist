### RPM external hepmc 2.06.05
Source: http://lcgapp.cern.ch/project/simu/HepMC/download/HepMC-%realversion.tar.gz
Patch0: hepmc-2.03.06-reflex
Patch1: hepmc-2.06.05-drop-pythia-symbols

%define keep_archives true
%if "%(case %cmsplatf in (osx*_*_gcc421) echo true ;; (*) echo false ;; esac)" == "true"
Requires: gfortran-macosx
%endif

%prep
%setup -q -n HepMC-%{realversion}
%patch0 -p0
%patch1 -p1

case %cmsplatf in
  slc5_*_gcc4[01234]*) 
    F77="`which gfortran`"
    CXX="`which c++`"
    PLATF_CONFIG_OPTS=""
  ;;
  *)
    F77="`which gfortran` -fPIC"
    CXX="`which c++` -fPIC"
    PLATF_CONFIG_OPTS="--enable-static --disable-shared"
  ;;
esac
./configure $PLATF_CONFIG_OPTS --prefix=%{i} --with-momentum=GEV --with-length=MM F77="$F77" CXX="$CXX"

%build
make %makeprocesses

%install
make install
rm -rf %i/lib/*.la
