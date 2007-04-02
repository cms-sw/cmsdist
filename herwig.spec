### RPM external herwig 6.510

Source: http://cern.ch/service-spi/external/MCGenerators/distribution/%{n}-%{v}-src.tgz
%prep
%setup -q -n %n
./configure 

%build
make 

%install
tar -c lib bin | tar -x -C %i

