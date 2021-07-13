### RPM cms scram-tools 1.0
## NOCOMPILER

%define branch main
%define tag 3df77f0a29f4d9b3912e4dbcafe4f22d99487af7
%define github_user cms-sw
%define github_repo %{n}

Source: git+https://github.com/%{github_user}/%{github_repo}.git?obj=%{branch}/%{tag}&export=%{n}-%{realversion}&output=/%{n}-%{realversion}-%{tag}.tgz

%prep
%setup -n %{n}-%{realversion}

%build

%install
cp -r %{_builddir}/%{n}-%{realversion} %{i}/%{n}
