### RPM external yoda 1.5.5

Source: http://cern.ch/service-spi/external/MCGenerators/distribution/%{n}/%{n}-%{realversion}-src.tgz

Requires: boost python cython

%prep
%setup -q -n %{n}/%{realversion}

./configure --prefix=%i --with-boost=${BOOST_ROOT} CXX="$(which g++)"

%build
make all

%install
make install

%post
%{relocateConfig}bin/yoda-config
