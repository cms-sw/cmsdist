### RPM cms vdt v0.3.2

Source: svn://svnweb.cern.ch/guest/%{n}/tags/%{realversion}?scheme=http&strategy=export&module=%{n}&output=/%{n}-%{realversion}.tar.gz

BuildRequires: cmake

%define isamd64 %(case %{cmsplatf} in (*amd64*) echo 1 ;; (*) echo 0 ;; esac)

%if "%{?cms_cxx:set}" != "set"
%define cms_cxx g++
%endif

%define keep_archives true

%prep
%setup -q -n %{n}

%build
%if %isamd64
cmake . \
  -DCMAKE_CXX_COMPILER="%{cms_cxx}" \
  -DCMAKE_INSTALL_PREFIX=%{i} \
  -DPRELOAD:BOOL=ON \
  -DSSE:BOOL=ON \
  -DNEON:BOOL=OFF
%else
cmake . \
  -DCMAKE_CXX_COMPILER="%{cms_cxx}" \
  -DCMAKE_INSTALL_PREFIX=%{i} \
  -DPRELOAD:BOOL=ON \
  -DSSE:BOOL=OFF \
  -DNEON:BOOL=OFF
%endif

make %{makeprocesses} VERBOSE=1

%install
make install
