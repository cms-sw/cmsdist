### RPM external mkfit 2.1.0
## INCLUDE compilation_flags
%define tag V2.1.0-0+pr291
%define branch devel
%define github_user trackreco

Source: git+https://github.com/%{github_user}/%{n}.git?obj=%{branch}/%{tag}&export=%{n}-%{realversion}&output=/%{n}-%{realversion}.tgz
Requires: tbb
BuildRequires: gmake
Patch0: mkfit-2.0.0-non-x86_64-fix

%prep
%setup -q -n %{n}-%{realversion}

%ifnarch x86_64
%patch0 -p1
%endif

sed -i -e 's|-std=c++14|-std=c++1z|' Makefile.config

%build
%ifarch x86_64
BUILD_ARGS=VEC_GCC="-msse3"
%endif
%ifarch aarch64
BUILD_ARGS=VEC_GCC="-march=native"
%endif
%ifarch ppc64le
BUILD_ARGS=VEC_GCC="%{ppc64le_build_flags}"
%endif
make %{makeprocesses} TBB_PREFIX=$TBB_ROOT "${BUILD_ARGS}"

%install
mkdir %{i}/include %{i}/include/mkFit %{i}/Geoms
cp -a *.h %{i}/include
cp -a mkFit/*.h %{i}/include/mkFit
cp -a Geoms/*.so %{i}/Geoms
cp -ar lib %{i}/lib
