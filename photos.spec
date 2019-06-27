### RPM external photos 215.5

Source: http://cern.ch/service-spi/external/MCGenerators/distribution/%{n}/%{n}-%{realversion}-src.tgz
Patch0: photos-215.5-update-configure
%define keep_archives true

%prep
%setup -q -n %{n}/%{realversion}
%patch0 -p2

%build
PLATF_CONFIG_OPTS="--enable-static --disable-shared"
./configure --lcgplatform=%cmsplatf $PLATF_CONFIG_OPTS 
%ifos darwin
perl -p -i -e "s|libphotos.so|libphotos.dylib|g" Makefile ;;
%endif
make 

%install
tar -c lib include | tar -x -C %i
find %i/lib/archive -name "*.a" -exec mv {} %i/lib \;
rm -rf %i/lib/archive

# bla bla
