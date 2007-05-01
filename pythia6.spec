### RPM external pythia6 409-CMS1
%define realversion %(echo %v | cut -d- -f1 )
Source: http://service-spi.web.cern.ch/service-spi/external/MCGenerators/distribution/%{n}-%{realversion}-src.tgz
%prep
%setup -q -n %{n}/%{realversion}
./configure 

%build
make 

find lib/archive -name "*.a" -exec mv {} lib/.  \;


%install

tar -c lib include | tar -x -C %i

