### RPM external charybdis 1.003
%define mic %(case %cmsplatf in (*_mic_*) echo true;; (*) echo false;; esac)
%if "%mic" == "true"
Requires: icc
%endif
Source: http://cern.ch/service-spi/external/MCGenerators/distribution/%{n}/%{n}-%{realversion}-src.tgz
Patch0: charybdis-1003-macosx
Patch1: charybdis-1.003-archive-only

Requires: pythia6
Requires: lhapdf
Requires: zlib

%define keep_archives true
%if "%(case %cmsplatf in (osx*_*_gcc421) echo true ;; (*) echo false ;; esac)" == "true"
Requires: gfortran-macosx
%endif

%prep
%setup -q -n %{n}/%{realversion}
%patch0 -p3
# On osx we build only the archive libraries to avoid issues with the common
# blocks.
case %cmsos in
  osx*)
%patch1 -p3
  ;;
esac
./configure --lcgplatform=%cmsplatf --pythia_hadronization

%build
%if "%mic" == "true"
perl -p -i -e "s|FC = gfortran|FC = `which ifort` -mmic -fPIC|" config.mk
CXX="icpc -mmic -fPIC" \
%else
perl -p -i -e "s|FC = gfortran|FC = `which gfortran` -fPIC|" config.mk
%endif
make PYTHIA6_ROOT=$PYTHIA6_ROOT LHAPDF_ROOT=$LHAPDF_ROOT ZLIB_ROOT=$ZLIB_ROOT

%install
tar -c lib include | tar -x -C %i
find %i/lib/archive -name "*.a" -exec mv {} %i/lib \;
rm -rf %i/lib/archive

