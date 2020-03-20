### RPM cms vdt 0.4.0

Source: https://github.com/dpiparo/%{n}/archive/v%{realversion}.tar.gz 

BuildRequires: cmake


%define keep_archives true

%prep
%setup -q -n %{n}-%{realversion}

%build
%ifarch x86_64
cmake . \
  -DCMAKE_INSTALL_PREFIX=%{i} \
  -DPRELOAD:BOOL=ON \
  -DSSE:BOOL=ON \
  -DNEON:BOOL=OFF
%else
cmake . \
  -DCMAKE_INSTALL_PREFIX=%{i} \
  -DPRELOAD:BOOL=ON \
  -DSSE:BOOL=OFF \
  -DNEON:BOOL=OFF
%endif

make %{makeprocesses} VERBOSE=1

%install
make install
