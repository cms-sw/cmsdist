### RPM external alpaka 2.2.0-pre-20260828
## NOCOMPILER

%define git_commit d19dae052afec299056552e95c34b60d00c0c7ba

Source: https://github.com/alpaka-group/%{n}/archive/%{git_commit}.tar.gz

%prep
%setup -n %{n}-%{git_commit}

%build

%install
cp -ar include %{i}/include

%post
