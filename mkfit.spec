### RPM external mkfit 2.0.0
%define tag V2.0.0-1+pr237
%define branch devel
%define github_user trackreco

Source: git+https://github.com/%{github_user}/%{n}.git?obj=%{branch}/%{tag}&export=%{n}-%{realversion}&output=/%{n}-%{realversion}.tgz
Requires: tbb

Patch0: mkfit-arm-patch

%prep
%setup -q -n %{n}-%{realversion}
%ifarch aarch64
%patch0 -p1
%endif

%build

%ifarch aarch64
make TBB_PREFIX=$TBB_ROOT VEC_GCC="-march=native"
%else
make TBB_PREFIX=$TBB_ROOT VEC_GCC="-march=core2"
%endif

%install
mkdir %{i}/include %{i}/include/mkFit %{i}/Geoms
cp -a *.h %{i}/include
cp -a mkFit/*.h %{i}/include/mkFit
cp -a Geoms/*.so %{i}/Geoms
cp -ar lib %{i}/lib
