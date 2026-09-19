### RPM external alpaka 2.2.0-pre-20260916
## NOCOMPILER

%define git_commit 266b4d9b69d2f42806acf03e9f5888ce5b9e23c8

Source: https://github.com/alpaka-group/%{n}/archive/%{git_commit}.tar.gz

%prep
%setup -n %{n}-%{git_commit}

%build

%install
cp -ar include %{i}/include

%post
