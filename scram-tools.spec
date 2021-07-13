### RPM cms scram-tools 1.0
## NOCOMPILER

%define branch main
%define tag 588309281b221cdf0f4e36e69aa8bbc3a017336c
%define github_user cms-sw
%define github_repo %{n}

Source: git+https://github.com/%{github_user}/%{github_repo}.git?obj=%{branch}/%{tag}&export=%{n}-%{realversion}&output=/%{n}-%{realversion}-%{tag}.tgz

%prep
%setup -n %{n}-%{realversion}

%build

%install
cp -r %{_builddir}/%{n}-%{realversion} %{i}/%{n}
