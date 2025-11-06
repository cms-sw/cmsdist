### RPM external alpaka develop-20251106
## NOCOMPILER

%define git_commit 3aafde5d2b32853ef5362a581624d2c24e1604d9

Source: https://github.com/cms-externals/%{n}/archive/%{git_commit}.tar.gz

%prep
%setup -n %{n}-%{git_commit}

%build

%install
cp -ar include %{i}/include

%post
