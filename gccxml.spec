### RPM external gccxml 0.9.0-20140124-0

BuildRequires: cmake

%define commit ab651a2aa866351bdd089a4bf1d57f6a9bec2a66
Source: git+https://github.com/gccxml/gccxml.git?obj=master/%{commit}&export=%{n}-%{realversion}&output=/%{n}-%{realversion}.tar.gz

%define isdarwin %(case %{cmsos} in (osx*) echo 1 ;; (*) echo 0 ;; esac)

%prep
%setup -n %{n}-%{realversion}

%if %isdarwin
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
