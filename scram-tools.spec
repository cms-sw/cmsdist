### RPM cms scram-tools 1.0

%define branch main
%define tag 33e20671985a2b7774681adcdfce655c0186b650
%define github_user cmss-sw
%define github_repo %{n}

Source: git+https://github.com/%{github_user}/%{github_repo}.git?obj=%{branch}/%{tag}&export=%{n}-%{realversion}&output=/%{n}-%{realversion}-%{tag}.tgz

%prep
%setup -n %{n}-%{realversion}

%build

%install
cp -r %{_builddir}/%{n}-%{realversion} %{i}/%{n}
