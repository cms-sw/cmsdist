### RPM external alpaka 2.2.0
## NOCOMPILER

%define git_commit %{realversion}

Source: https://github.com/alpaka-group/%{n}/archive/%{git_commit}.tar.gz
# Philox4x32-10 as in Random123, and fixes of the engine seeding and the distributions
Patch0: alpaka-philox-random123

%prep
%setup -n %{n}-%{git_commit}
%patch0 -p1

%build

%install
cp -ar include %{i}/include

%post
