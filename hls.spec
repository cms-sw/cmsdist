### RPM external hls 2019.08
%define tag 200a9aecaadf471592558540dc5a88256cbf880f
%define branch master
%define github_user Xilinx
Source: git+https://github.com/%{github_user}/HLS_arbitrary_Precision_Types.git?obj=%{branch}/%{tag}&export=%{n}-%{realversion}&output=/%{n}-%{realversion}-%{tag}.tgz
Requires: gmake

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


