### RPM external git-lfs 3.7.1
Source: https://github.com/git-lfs/git-lfs/releases/download/v%{realversion}/git-lfs-linux-%{go_package_arch}-v%{realversion}.tar.gz
Requires: git

%prep
%setup -n %{n}-%{realversion}

%build

%install
PREFIX=%{i} ./install.sh
