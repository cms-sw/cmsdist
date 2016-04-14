### RPM external dmtcp 3.0.0-dev

%define git_repo dmtcp
%define git_branch master
%define git_commit 685e319e5fe2ede8daf3e24d8e5a838544c4984e
Source: git://github.com/%{git_repo}/dmtcp.git?obj=%{git_branch}/%{git_commit}&export=dmtcp-%{git_commit}&output=/dmtcp-%{git_commit}.tgz

%define drop_files %{i}/share

%prep
%setup -n dmtcp-%{git_commit}

%build
./configure \
  --prefix=%{i} \
  --disable-test-suite \
  --disable-dependency-tracking

make %{makeprocesses}

%install

make install
