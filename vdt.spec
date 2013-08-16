### RPM cms vdt v0.3.2

Source: svn://svnweb.cern.ch/guest/%{n}/tags/%{realversion}?scheme=http&strategy=export&module=%{n}&output=/%{n}-%{realversion}.tar.gz

BuildRequires: cmake

%define isamd64 %(case %{cmsplatf} in (*amd64*) echo 1 ;; (*) echo 0 ;; esac)
%define isarmv7 %(case %{cmsplatf} in (*armv7*) echo 1 ;; (*) echo 0 ;; esac)
%define iscpu_marvell %(cat /proc/cpuinfo | grep 'Marvell PJ4Bv7' 2>&1 >/dev/null && echo 1 || echo 0)

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
  -DSSE:BOOL=ON 
%endif

%if %isarmv7
# Select NEON or VFPv3/VFPv3-D16
%if %iscpu_marvell
%define neon_support OFF
%else
%define neon_support ON
%endif

cmake . \
  -DCMAKE_CXX_COMPILER="%{cms_cxx}" \
  -DCMAKE_INSTALL_PREFIX=%{i} \
  -DPRELOAD:BOOL=ON \
  -DSSE:BOOL=OFF \
  -DNEON:BOOL=%{neon_support}
%endif

make %{makeprocesses} VERBOSE=1

%install
make install
