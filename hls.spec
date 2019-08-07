### RPM external hls 1.0
%define tag 200a9aecaadf471592558540dc5a88256cbf880f
%define branch master
%define github_user Xilinx
Source: git+https://github.com/%{github_user}/HLS_arbitrary_Precision_Types.git?obj=%{branch}/%{tag}&export=%{n}-%{realversion}&output=/%{n}-%{realversion}-%{tag}.tgz

%prep
%setup -n %{n}-%{realversion}

%build

%install
cp -r * %{i}/


