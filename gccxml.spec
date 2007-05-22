### RPM external gccxml 0.6.0-XXXX

Requires: cmake
Source: http://www.gccxml.org/files/v0.6/%n-%realversion.tar.gz
Patch0: gccxml1
Patch1: gccxml2
Patch2: gccxml3

%prep
%setup -n %{n}-%{realversion}
%patch1 -p1 

%build
mkdir gccxml-build
cd gccxml-build
cmake -DCMAKE_INSTALL_PREFIX:PATH=%i ..
make %makeprocesses

%install
cd gccxml-build
make install
cd %i
patch -p1 <%{_sourcedir}/gccxml1
patch -p1 <%{_sourcedir}/gccxml3

%post
%{relocateConfig}share/gccxml-0.6/gccxml_config
