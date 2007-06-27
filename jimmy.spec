### RPM external jimmy 4.2-CMS3
Requires: herwig
%define realversion %(echo %v | cut -d- -f1 )
Source: http://service-spi.web.cern.ch/service-spi/external/MCGenerators/distribution/%{n}-%{realversion}-src.tgz
%prep
%setup -q -n %{n}
./configure --with-herwig=$HERWIG_ROOT

%build
make 

%install
tar -c lib include | tar -x -C %i

