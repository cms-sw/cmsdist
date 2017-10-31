### RPM external yoda 1.6.7

## OLD GENSER Source: http://cern.ch/service-spi/external/MCGenerators/distribution/%{n}/%{n}-%{realversion}-src.tgz
Source: http://lcgpackages.web.cern.ch/lcgpackages/tarFiles/sources/MCGeneratorsTarFiles/YODA-%{realversion}.tar.gz 

Requires: python root
BuildRequires: py2-cython
%prep
## OLD GENSER #%setup -q -n %{n}/%{realversion}
%setup -q -n YODA-%{realversion}

./configure --prefix=%i --enable-root

%build
make all

%install
make install

%post
%{relocateConfig}bin/yoda-config
