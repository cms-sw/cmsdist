### RPM cms scram-tools 1.0
## NOCOMPILER

%define branch IB/CMSSW_12_0_X/master
%define tag f32993e0e9d084f0ec4b0bae9756f705efb0827d
%define github_user cms-sw
%define github_repo %{n}

Source: git+https://github.com/%{github_user}/%{github_repo}.git?obj=%{branch}/%{tag}&export=%{n}-%{realversion}&output=/%{n}-%{realversion}-%{tag}.tgz

%prep
%setup -n %{n}-%{realversion}

%build

%install
cp -r %{_builddir}/%{n}-%{realversion} %{i}/%{n}
