### RPM external yoda 1.7.7
## INITENV +PATH PYTHON27PATH %i/${PYTHON_LIB_SITE_PACKAGES}
## INITENV +PATH PYTHON3PATH %i/${PYTHON3_LIB_SITE_PACKAGES}

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
