### RPM external alpaka 2.0.0
## NOCOMPILER

%define git_commit %{realversion}

Source: https://github.com/cms-externals/%{n}/archive/%{git_commit}.tar.gz

%prep
%setup -n %{n}-%{git_commit}

%build

%install
cp -ar include %{i}/include

%post
