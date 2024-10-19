### RPM cms vdt 0.4.3

Source: https://github.com/dpiparo/%{n}/archive/v%{realversion}.tar.gz
# To avoid UBSan runtime errors about signed integer overflow: cms-sw/cmssw#46417
Patch0: vdt-integer-overflow
BuildRequires: cmake python3


%define keep_archives true

%prep
%setup -q -n %{n}-%{realversion}
%patch0 -p1

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
