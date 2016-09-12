### RPM external mctester 1.25.0a

Source:  http://service-spi.web.cern.ch/service-spi/external/MCGenerators/distribution/%{n}/%{n}-%{realversion}-src.tgz

Patch0: mctester-cling

Requires: hepmc
Requires: root

BuildRequires: autotools

%define keep_archives true

%define isdarwin %(case %{cmsos} in (osx*) echo 1 ;; (*) echo 0 ;; esac)

%if "%{?cms_cxx:set}" != "set"
%define cms_cxx g++
%endif

%if "%{?cms_cxxflags:set}" != "set"
%define cms_cxxflags -O2 -std=c++0x
%endif

%prep
%setup -q -n %{n}/%{realversion}
%patch0 -p2

./configure \
  --with-HepMC=${HEPMC_ROOT} \
  --with-root=${ROOT_ROOT} \
  --prefix=%i \
  CXX="%cms_cxx" \
  CXXFLAGS="%cms_cxxflags"

%build
make

%install
make install

%if %isdarwin
find %i/lib -name "*.dylib" -exec install_name_tool -change '../lib/libHEPEvent.dylib' 'libHEPEvent.dylib' {} \;
%endif
