### RPM external alpaka 2.2.0-pre-20260930
## NOCOMPILER

%define git_commit e2f7294f4b15b61858666bbbc76ea1122ee26844

Source: https://github.com/alpaka-group/%{n}/archive/%{git_commit}.tar.gz

%prep
%setup -n %{n}-%{git_commit}

%build

%install
cp -ar include %{i}/include

%post
