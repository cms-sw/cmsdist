### RPM external patchelf 0.13
## NO_AUTO_RUNPATH

%define git_branch master
%define git_commit %{realversion}
Source0: git://github.com/NixOS/patchelf.git?obj=%{git_branch}/%{git_commit}&export=patchelf-%{realversion}&output=/patchelf-%{realversion}.tgz
BuildRequires: autotools gmake

%define drop_files %{i}/share

%prep
%setup -n patchelf-%{realversion}

%build

./bootstrap.sh
./configure --prefix=%{i}
make %{makeprocesses}

%install
make install
