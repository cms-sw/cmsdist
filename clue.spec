### RPM external clue 1.0.0
## NOCOMPILER

%define git_commit V_%(echo %{realversion} | tr '.' '_')

Source: https://gitlab.cern.ch/kalos/%{n}/-/archive/%{git_commit}/%{n}-%{git_commit}.tar.gz
Requires: alpaka

%prep
%setup -n %{n}-%{git_commit}

%build

%install
cp -ar clueLib/include %{i}/include

%post
