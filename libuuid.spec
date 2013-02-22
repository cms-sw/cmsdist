### RPM external libuuid 2.22.2
Source: http://www.kernel.org/pub/linux/utils/util-linux/v2.22/util-linux-%{realversion}.tar.gz
%define keep_archives true

%prep
%setup -n util-linux-%{realversion}

%build
./configure $([ $(uname) == Darwin ] && echo --disable-shared) --disable-uuidd \
            --disable-tls --disable-login --disable-su --libdir=%{i}/lib64 \
            --prefix=%{i} --disable-silent-rules
make %{makeprocesses}

%install
# There is no make install action for the libuuid libraries only
mkdir -p %{i}/lib64
cp -p %{_builddir}/util-linux-%{realversion}/.libs/libuuid.a* %{i}/lib64
%ifos linux
cp -p %{_builddir}/util-linux-%{realversion}/.libs/libuuid.so* %{i}/lib64
%endif
mkdir -p %{i}/include
make install-uuidincHEADERS

%define drop_files %{i}/man
