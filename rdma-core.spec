### RPM external rdma-core 50.0
## INITENV +PATH LD_LIBRARY_PATH %{i}/lib64

Source: https://github.com/linux-rdma/%{n}/releases/download/v%{realversion}/rdma-core-%{realversion}.tar.gz
BuildRequires: cmake ninja

%prep
%setup -q -n %{n}-%{realversion}

%build
rm -rf build
mkdir build
cd build

# currently there is no way to use a custom location for libnl3, so disable neighbours resolution
cmake \
  -G Ninja \
  -DCMAKE_INSTALL_PREFIX=%{i} \
  -DCMAKE_INSTALL_RUNDIR=/var/run \
  -DENABLE_RESOLVE_NEIGH=FALSE \
  -DENABLE_STATIC=FALSE \
  -DNO_MAN_PAGES=TRUE \
  ..

cmake -L .

ninja -v %{makeprocesses}

%install
cd build
ninja -v %{makeprocesses} install

# remove pkg-config to avoid rpm-generated dependency on /usr/bin/pkg-config
rm -rf %{i}/lib64/pkgconfig

# keep only the libraries and include files
rm -rf %{i}/bin
rm -rf %{i}/etc
rm -rf %{i}/lib
rm -rf %{i}/libexec
rm -rf %{i}/sbin
rm -rf %{i}/share
