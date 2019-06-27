### RPM external patchelf 0.10
## INITENV +PATH PATH %{i}/bin

%define git_branch master
%define git_commit 327d80443672c397970738f9e216a7e86cbf3ad7
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
# bla bla
