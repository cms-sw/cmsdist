### RPM cms scram-tools 1.0
## NOCOMPILER

%define branch IB/CMSSW_12_0_X/master
%define tag f042f65d7b292e942af0cb547c4a12e5987026bf
%define github_user cms-sw
%define github_repo %{n}

Source: git+https://github.com/%{github_user}/%{github_repo}.git?obj=%{branch}/%{tag}&export=%{n}-%{realversion}&output=/%{n}-%{realversion}-%{tag}.tgz

%prep
%setup -n %{n}-%{realversion}

%build

%install
cp -r %{_builddir}/%{n}-%{realversion} %{i}/%{n}
