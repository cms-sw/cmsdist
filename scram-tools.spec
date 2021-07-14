### RPM cms scram-tools 1.0
## NOCOMPILER

%define branch main
%define tag 8c5f3b616bf4b52d1d7d857e6b179d21239ee022
%define github_user cms-sw
%define github_repo %{n}

Source: git+https://github.com/%{github_user}/%{github_repo}.git?obj=%{branch}/%{tag}&export=%{n}-%{realversion}&output=/%{n}-%{realversion}-%{tag}.tgz

%prep
%setup -n %{n}-%{realversion}

%build

%install
cp -r %{_builddir}/%{n}-%{realversion} %{i}/%{n}
