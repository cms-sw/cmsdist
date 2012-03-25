### RPM external gccxml 20110825 
Requires: cmake
Source: http://service-spi.web.cern.ch/service-spi/external/tarFiles/%n-%realversion.tgz
Patch0: gccxml-0.9.0_20100308-gcc45-iomanip

%prep
%setup -n %{n}
#patch0 -p1
case %cmsos in 
  osx*_*_gcc421) ;;
  osx*)
perl -p -i -e 's|-no-cpp-precomp||g' GCC/CMakeLists.txt \
                                     GCC/configure.in \
                                     GCC/configure
  ;;
esac
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
find $RPM_INSTALL_PREFIX/%{pkgrel}/share -name gccxml_config -exec %relocateCmsFiles {} \;
