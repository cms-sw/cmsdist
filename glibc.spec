### RPM external glibc 2.17-78.el7_2.12-1.166.el6_7.3
## NOCOMPILER

%define isslc6 %(case %{cmsplatf} in (slc6*) echo 1 ;; (*) echo 0 ;; esac)
%define isslc7 %(case %{cmsplatf} in (slc7*) echo 1 ;; (*) echo 0 ;; esac)

%if %isslc7
%define realversion 2.17-78.el7
%define tag ffca09a735586cbe44d9e330dc4c94ce18fa6aa3
%endif

%if %isslc6
%define realversion 2.12-1.166.el6_7.3
%define tag 2c052e03acb1795ac2c47f803b252ae85918e5ea
%endif

%global official_version %(echo "%{realversion}" | cut -d'-' -f1)

%define branch cms/%{realversion}
%define github_user cms-externals
Source: git+https://github.com/%{github_user}/glibc.git?obj=%{branch}/%{tag}&export=%{n}-%{realversion}&output=/%{n}-%{realversion}.tgz

%prep
%setup -n %{n}-%{realversion}

%build

rm -rf ../%{n}-build
mkdir ../%{n}-build
cd ../%{n}-build
../%{n}-%{realversion}/configure \
  CC=gcc \
  CXX=g++ \
  CFLAGS='-mtune=generic -fasynchronous-unwind-tables -DNDEBUG -g -O3' \
  --prefix=/usr \
  --enable-add-ons=nptl,c_stubs,libidn \
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
cd ../%{n}-build
make install install_root=%{i}

# Remove everything except dynamic loader. All changes are contained
# within the loader.
find %{i} ! -type d | grep -Z -v 'ld-%{official_version}' | xargs rm -f
find %{i} -empty -type d -delete

mv %{i}/lib64/ld-%{official_version}.so %{i}/lib64/ld.so
# bla bla
