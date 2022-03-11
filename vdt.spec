### RPM cms vdt 0.4.3

Source: https://github.com/dpiparo/%{n}/archive/v%{realversion}.tar.gz 

BuildRequires: cmake python3


%define keep_archives true

%prep
%setup -q -n %{n}-%{realversion}

%build
cmake . \
  -DCMAKE_INSTALL_PREFIX=%{i} \
  -DPYTHONLIBS_VERSION_STRING=%{cms_python3_major_minor_version} \
  -DPRELOAD:BOOL=ON \
%ifarch x86_64
  -DSSE:BOOL=ON \
%else
  -DSSE:BOOL=OFF \
%endif
  -DNEON:BOOL=OFF

make %{makeprocesses} VERBOSE=1

%install
make install
