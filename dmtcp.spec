### RPM external dmtcp 3.0.0-dev

%define git_repo dmtcp
%define git_branch master
%define git_commit 3dff1b3d30d6362d2c64120bb6ecba0d387cd1ea
Source: git://github.com/%{git_repo}/dmtcp.git?obj=%{git_branch}/%{git_commit}&export=dmtcp-%{git_commit}&output=/dmtcp-%{git_commit}.tgz

Patch0: dmtcp-remove-git-hooks
Patch1: dmtcp-3.0.0-dev-ptr-int-comp

%define drop_files %{i}/share

%prep
%setup -n dmtcp-%{git_commit}
%patch0 -p1
%patch1 -p1

%build
./configure \
  --prefix=%{i} \
  --disable-test-suite \
  --disable-dependency-tracking

make %{makeprocesses}

%install

make install
# bla bla
