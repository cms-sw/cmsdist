### RPM external glibc 2.12-1.149.el6
## NOCOMPILER

%global official_version %(echo "%{realversion}" | cut -d'-' -f1)

%define tag 4bcf8ff366875ccd2ec8c45b63c0c482f07a24fb
%define branch cms/2.12-1.149.el6
%define github_user cms-externals
Source: git+https://github.com/%{github_user}/glibc.git?obj=%{branch}/%{tag}&export=%{n}-%{realversion}&output=/%{n}-%{realversion}.tgz

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
