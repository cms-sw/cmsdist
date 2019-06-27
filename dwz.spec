### RPM external dwz 0.12

%define dwz_branch master
%define dwz_commit dwz-0.12

Source: git://sourceware.org/git/dwz.git?obj=%{dwz_branch}/%{dwz_commit}&export=dwz-%{dwz_commit}&output=/dwz-%{dwz_commit}.tgz

%prep
%setup -T -b 0 -n dwz-%{dwz_commit}

%build
make %{makeprocesses}

%install
mkdir -p %{i}/bin
cp dwz %{i}/bin
# bla bla
