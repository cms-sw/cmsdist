### RPM external mctester 1.25.0a

Source:  http://service-spi.web.cern.ch/service-spi/external/MCGenerators/distribution/%{n}/%{n}-%{realversion}-src.tgz

Patch0: mctester-root6-tbuffer

Requires: hepmc
Requires: root

BuildRequires: autotools

%define keep_archives true

%define isdarwin %(case %{cmsos} in (osx*) echo 1 ;; (*) echo 0 ;; esac)

%prep
%setup -q -n %{n}/%{realversion}
%patch0 -p2

./configure \
  --with-HepMC=${HEPMC_ROOT} \
  --with-root=${ROOT_ROOT} \
  --prefix=%i

%build
make

%install
make install

%if %isdarwin
find %i/lib -name "*.dylib" -exec install_name_tool -change '../lib/libHEPEvent.dylib' 'libHEPEvent.dylib' {} \;
%endif
