### RPM external yoda 1.6.5

Source: http://cern.ch/service-spi/external/MCGenerators/distribution/%{n}/%{n}-%{realversion}-src.tgz

Requires: python cython root

%prep
%setup -q -n %{n}/%{realversion}

./configure --prefix=%i --enable-root

%build
make all

%install
make install

%post
%{relocateConfig}bin/yoda-config
