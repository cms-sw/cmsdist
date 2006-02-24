### RPM external graphviz 1.9 
Source: http://service-spi.web.cern.ch/service-spi/external/tarFiles/%{n}-%{v}.tar.gz  

%prep
%setup -n %{n}-%{v}

%build
./configure --prefix=%{i}
make
