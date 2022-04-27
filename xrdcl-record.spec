### RPM external xrdcl-record 5.4.2
Source: https://github.com/xrootd/xrdcl-record/archive/refs/tags/v5.4.2.tar.gz

BuildRequires: gmake cmake
Requires: xrootd

%prep
%setup -n %setup -q -n %{n}-%{realversion}

%build
rm -rf ../build; mkdir ../build ; cd ../build
cmake ../%{n}-%{realversion} \
  -DCMAKE_BUILD_TYPE=Release \
  -DCMAKE_INSTALL_PREFIX="%{i}" \
  -DCMAKE_PREFIX_PATH="${XROOTD_ROOT}"

gmake %{makeprocesses}

%install
cd ../build
gmake %{makeprocesses} install
