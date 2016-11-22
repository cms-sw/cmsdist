### RPM external yoda 1.6.5

Source: http://cern.ch/service-spi/external/MCGenerators/distribution/%{n}/%{n}-%{realversion}-src.tgz

Requires: python cython root

%if "%{?cms_cxxflags:set}" != "set"
%define cms_cxxflags -std=c++0x -O2
%endif

%prep
%setup -q -n %{n}/%{realversion}

./configure --prefix=%i --enable-root

%build
make all

%install
make install

%post
%{relocateConfig}bin/yoda-config
