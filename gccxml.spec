### RPM external gccxml 0.9.0-20130101-0

BuildRequires: cmake

Source: git+https://github.com/gccxml/gccxml.git?obj=master/2cbeb9d631e0198fcbeca3d230ef49fe07e87dd8&export=%{n}-%{realversion}&output=/%{n}-%{realversion}.tar.gz

Patch0: gccxml-0.9.0-add-gcc-4.8

%prep
%setup -n %{n}-%{realversion}
%patch0 -p1

%ifos darwin
# Drop no more supported -no-cpp-precomp on Darwin.
sed -i '' 's/-no-cpp-precomp//g' \
  GCC/CMakeLists.txt \
  GCC/configure.in \
  GCC/configure
%endif

%build
mkdir gccxml-build
cd gccxml-build
cmake .. \
   -DCMAKE_INSTALL_PREFIX:PATH=%{i}
make %makeprocesses

%install
cd gccxml-build
make install

%define drop_files %i/share/{man,doc}

%post
%{relocateConfig}share/gccxml-0.9/gccxml_config
