### RPM external photos 215.5

Source: http://cern.ch/service-spi/external/MCGenerators/distribution/%{n}/%{n}-%{realversion}-src.tgz
Patch0: photos-215.5-macosx
%define keep_archives true
%if "%(case %cmsplatf in (osx*_*_gcc421) echo true ;; (*) echo false ;; esac)" == "true"
Requires: gfortran-macosx
%endif

%prep
%setup -q -n %{n}/%{realversion}
%patch0 -p3

%build
case %cmsplatf in
  slc5_*_gcc4[01234]*) ;;
  *) PLATF_CONFIG_OPTS="--enable-static --disable-shared" ;;
esac
./configure --lcgplatform=%cmsplatf $PLATF_CONFIG_OPTS 
case %cmsplatf in
  osx*) perl -p -i -e "s|libphotos.so|libphotos.dylib|g" Makefile ;;
esac
make 

%install
tar -c lib include | tar -x -C %i
find %i/lib/archive -name "*.a" -exec mv {} %i/lib \;
rm -rf %i/lib/archive

