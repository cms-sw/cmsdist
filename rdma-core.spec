### RPM external rdma-core 57.0
## INITENV +PATH LD_LIBRARY_PATH %{i}/lib64

Source: https://github.com/linux-rdma/%{n}/releases/download/v%{realversion}/rdma-core-%{realversion}.tar.gz
Patch: rdma-core-VERBS_CONFIG_DIR
BuildRequires: cmake ninja

%prep
%setup -q -n %{n}-%{realversion}
%patch -p1

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

# keep only the user binaries, libibverbs configuration, libraries and include files
rm -rf %{i}/etc/infiniband-diags
rm -rf %{i}/etc/init.d
rm -rf %{i}/etc/modprobe.d
rm -rf %{i}/etc/rdma
rm -rf %{i}/lib
rm -rf %{i}/libexec
rm -rf %{i}/sbin
rm -rf %{i}/share/perl5

# update the libibverbs plugins with the full path
sed -e's#driver \(\w\+\)#driver %{i}/lib64/libibverbs/lib\1#' -i %{i}/etc/libibverbs.d/*

%post
# relocate the libibverbs plugins path
%{relocateConfig}etc/libibverbs.d/*
