### RPM external graphviz 1.9 
Source: http://service-spi.web.cern.ch/service-spi/external/tarFiles/%{n}-%{v}.tar.gz  
Requires: expat

%prep
%setup -n %{n}-%{v}

%build
./configure --with-expatlibdir=$EXPAT_ROOT/lib --with-expatincludedir=$EXPAT_ROOT/include --without-x --prefix=%{i}
make
