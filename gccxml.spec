### RPM external gccxml 0.9.0_20100308
%define gccxmlmajorver %(echo %realversion | cut -f1 -d_)
%define gccxmlconfigver %(echo %realversion | cut -f1 -d_ | cut -f1,2 -d.)
Requires: cmake
Source: http://service-spi.web.cern.ch/service-spi/external/tarFiles/%n-%realversion.tar.gz
Patch0: gccxml-0.9.0_20100308-gcc45-iomanip

%prep
%setup -n %{n}
%patch0 -p1

%build
cd GCC_XML/Support
cd ../../
mkdir gccxml-build
cd gccxml-build
cmake -DCMAKE_INSTALL_PREFIX:PATH=%i ..
make %makeprocesses

%install
cd gccxml-build
make install

%post
%{relocateConfig}share/gccxml-%{gccxmlconfigver}/gccxml_config
