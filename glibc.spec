### RPM external glibc 2.12-2
## NOCOMPILER

%global official_version %(echo "%{realversion}" | cut -d'-' -f1)

%define tag 31f3c8e59749ef5f77853ec2d5c019e48bdcd645
%define branch cms/%{n}-%{realversion}
%define github_user davidlt
Source: git+https://github.com/%{github_user}/glibc-2.12-slc6.git?obj=%{branch}/%{tag}&export=%{n}-%{realversion}&output=/%{n}-%{realversion}.tgz

%prep
%setup -n %{n}-%{realversion}

%build

rm -rf ../glibc-build
mkdir ../glibc-build
cd ../glibc-build
../glibc-%{realversion}/configure \
  CC=gcc \
  CXX=g++ \
  CFLAGS='-mtune=generic -fasynchronous-unwind-tables -DNDEBUG -g -O3' \
  --prefix=/usr \
  --enable-add-ons=nptl,rtkaio,c_stubs,libidn \
  --without-cvs \
  --enable-kernel=2.6.18 \
  --with-headers=/usr/include \
  --enable-bind-now \
  --with-tls \
  --with-__thread \
  --build=x86_64-redhat-linux \
  --host=x86_64-redhat-linux \
  --enable-multi-arch \
  --disable-profile \
  --enable-experimental-malloc

make %{makeprocesses}

%install
cd ../glibc-build
make install install_root=%{i}

# Remove everything except dynamic loader. All changes are contained
# within the loader.
find %{i} ! -type d | grep -Z -v 'ld-%{official_version}' | xargs rm -f
find %{i} -empty -type d -delete

mv %{i}/lib64/ld-%{official_version}.so %{i}/lib64/ld.so
