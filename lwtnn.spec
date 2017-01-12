### RPM external lwtnn 1.0
Source: https://github.com/lwtnn/lwtnn/archive/v%{realversion}.tar.gz
BuildRequires: py2-pkgconfig
Requires: eigen boost
Patch0: lwtnn-1.0-boost-fix
%prep
%setup -n %{n}-%{realversion}
%patch0 -p1

%build

export PKG_CONFIG_PATH=$PKG_CONFIG_PATH:$EIGEN_ROOT/share/pkgconfig
export BOOST_ROOT
make all

%install
cp -r {lib,bin,include} %{i}/

