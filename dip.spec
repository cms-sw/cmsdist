### RPM external dip v6.6.2
%define branch CMW-6110
%define tag fec745230594f2148b334cc467888aaf9447e124
Source: git+ssh://git@gitlab.cern.ch:7999/acc-co/cmw/cmw-dip/dip.git?obj=%{branch}/%{tag}&export=%{n}-%{realversion}&output=/%{n}-%{realversion}.tgz
BuildRequires: cmake gmake
Requires: log4cplus

%prep
%setup -n %{n}-%{realversion}

%build
rm -rf ../build; mkdir ../build; cd ../build
cmake ../%{n}-%{realversion} \
  -DCMAKE_INSTALL_PREFIX=%{i} \
  -DCMAKE_BUILD_TYPE=Release \
  -DDIP_VERSION="$(echo %{realversion} |  sed 's|^v||')" \
  -DWITH_JNI=OFF \
  -DDIP_ACC=OFF \
  -DCMAKE_PREFIX_PATH="%{cmake_prefix_path}"

make %{makeprocesses} VERBOSE=1

%install
cd ../build
make install
