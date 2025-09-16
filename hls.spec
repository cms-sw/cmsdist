### RPM external hls 2025.05
%define tag 22a05fb9800df94678e642099c5c8e57fc2edb71
%define branch cms/200a9ae
%define github_user cms-externals
%define runpath_opts -m examples
Source: git+https://github.com/%{github_user}/HLS_arbitrary_Precision_Types.git?obj=%{branch}/%{tag}&export=%{n}-%{realversion}&output=/%{n}-%{realversion}-%{tag}.tgz
Source: hls_modulemap
BuildRequires: gmake

%prep
%setup -n %{n}-%{realversion}

%build

pushd examples/ap_fixed; make
mv a.out ../ap_fixed.exe ; popd

pushd examples/ap_int; make
mv a.out ../ap_int.exe ; popd

rm -rf examples/ap_int examples/ap_fixed

%install

cp -r * %{i}/
cp %{_sourcedir}/hls_modulemap  %{i}/include/hls.modulemap
