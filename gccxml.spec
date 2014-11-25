### RPM external gccxml 0.9.0-20140124-0

BuildRequires: cmake

%define commit 610ec28d8f67e48ec461d9b9ab83a2d192f5cf2e
Source: git+https://github.com/gccxml/gccxml.git?obj=master/%{commit}&export=%{n}-%{realversion}&output=/%{n}-%{realversion}.tar.gz
Patch0: gccxml-add-gcc49-support

%define isdarwin %(case %{cmsos} in (osx*) echo 1 ;; (*) echo 0 ;; esac)

%prep
%setup -n %{n}-%{realversion}
%patch0 -p1

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
