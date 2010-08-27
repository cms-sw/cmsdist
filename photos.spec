### RPM external photos 215.5

Source: http://cern.ch/service-spi/external/MCGenerators/distribution/%{n}-%{realversion}-src.tgz
Patch0: photos-215.5-macosx
%if "%(echo %cmsos | grep osx >/dev/null && echo true)" == "true"
Requires: gfortran-macosx
%endif

%prep
%setup -q -n %{n}/%{realversion}
%patch0 -p3

%build
./configure --lcgplatform=%cmsplatf
case %cmsplatf in
  osx*)
    perl -p -i -e "s|libphotos.so|libphotos.dylib|g" Makefile
  ;;
esac
make 

%install
tar -c lib include | tar -x -C %i
