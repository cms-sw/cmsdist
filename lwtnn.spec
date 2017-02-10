### RPM external lwtnn 1.0
Source: https://github.com/lwtnn/lwtnn/archive/v%{realversion}.tar.gz
BuildRequires: py2-pkgconfig
Requires: eigen boost
Patch0: lwtnn-1.0-boost-fix
%prep
%setup -n %{n}-%{realversion}
%patch0 -p1

%build

export BOOST_ROOT
make all

%install
cp -r {lib,bin,include} %{i}/

