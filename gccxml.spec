### RPM external gccxml 0.6.0

Requires: cmake
Source: http://www.gccxml.org/files/v0.6/%n-%v.tar.gz
Patch0: gccxml1
Patch1: gccxml2
Patch2: gccxml3

%prep
%setup -n %{n}-%{v}
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

#%patch0 -p1
#%patch2 -p1
#
