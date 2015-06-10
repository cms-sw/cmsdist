### RPM external patchelf 0.8
## INITENV +PATH PATH %{i}/bin

%define git_branch master
%define git_commit ec38df54a2cfd2c56b01dffdf11210a3d0805f9d
Source0: git://github.com/NixOS/patchelf.git?obj=%{git_branch}/%{git_commit}&export=%{n}-%{realversion}&output=/%{n}-%{realversion}.tgz
BuildRequires: autotools

%define drop_files %{i}/share

%prep
%setup -n %{n}-%{realversion}

%build

./bootstrap.sh
./configure --prefix=%{i}
make %{makeprocesses}

%install
make install
