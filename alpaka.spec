### RPM external alpaka develop-20220503
## NOCOMPILER

%define git_commit c493040fe0b3ef9416bb0bbb8d45550c184a67e0

Source: https://github.com/alpaka-group/%{n}/archive/%{git_commit}.tar.gz
Requires: boost

%prep
%setup -n %{n}-%{git_commit}

%build

%install
cp -ar include %{i}/include

%post
