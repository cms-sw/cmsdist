### RPM external hls 2019.08
%define tag 200a9aecaadf471592558540dc5a88256cbf880f
%define branch master
%define github_user Xilinx
Source: git+https://github.com/%{github_user}/HLS_arbitrary_Precision_Types.git?obj=%{branch}/%{tag}&export=%{n}-%{realversion}&output=/%{n}-%{realversion}-%{tag}.tgz
Requires: gmake

%prep
%setup -n %{n}-%{realversion}

%build
cd %_builddir/%{n}-%{realversion}/examples/ap_fixed
make
mv %_builddir/%{n}-%{realversion}/examples/ap_fixed/a.out %_builddir/%{n}-%{realversion}/examples/ap_fixed.out
cd %_builddir/%{n}-%{realversion}/examples/ap_int
make
mv %_builddir/%{n}-%{realversion}/examples/ap_int/a.out %_builddir/%{n}-%{realversion}/examples/ap_int.out

%install

cp -r * %{i}/


