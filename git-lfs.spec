### RPM external git-lfs 3.6.0
Source: https://github.com/git-lfs/git-lfs/archive/v%{realversion}.tar.gz
BuildRequires: gmake go
Requires: git

%prep
%setup -n %{n}-%{realversion}

%build
make %{makeprocesses} VERSION=v%{realversion} GIT_LFS_SHA=${realversion}

%install
mkdir -p %{i}/bin
mv bin/git-lfs %{i}/bin
