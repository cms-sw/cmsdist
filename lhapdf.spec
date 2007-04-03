### RPM external lhapdf 5.2.3

Source: http://cern.ch/service-spi/external/MCGenerators/distribution/%{n}-%{v}-src.tgz
%prep
%setup -q -n %{n}/%{v}
./configure 

%build
make 

%install
tar -c lib bin PDFsets | tar -x -C %i

