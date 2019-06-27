### RPM cms vdt 0.4.0

Source: https://github.com/dpiparo/%{n}/archive/v%{realversion}.tar.gz 

BuildRequires: cmake

%define isamd64 %(case %{cmsplatf} in (*amd64*) echo 1 ;; (*) echo 0 ;; esac)

%define keep_archives true

%prep
%setup -q -n %{n}-%{realversion}

%build
%if %isamd64
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
# bla bla
