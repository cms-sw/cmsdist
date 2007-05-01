### RPM external lhapdf 5.2.3-cms
%define realversion %(echo %v | cut -d- -f1)
Source: http://cern.ch/service-spi/external/MCGenerators/distribution/%{n}-%{realversion}-src.tgz
%prep
%setup -q -n %{n}/%{realversion}
./configure 

%build
make 

%install
tar -c lib include PDFsets | tar -x -C %i
