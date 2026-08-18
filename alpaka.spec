### RPM external alpaka 2.2.0-pre-20260914
## NOCOMPILER

%define git_commit d0a7409d4e9e73915da356a3e0537df6ea4b6a44

Source: https://github.com/alpaka-group/%{n}/archive/%{git_commit}.tar.gz

%prep
%setup -n %{n}-%{git_commit}

%build

%install
cp -ar include %{i}/include

%post
