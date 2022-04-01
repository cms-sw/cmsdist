### RPM external dwz 0.14

%define dwz_branch %{n}-%{realversion}-branch
%define dwz_commit b612e38de2a1a376362cc2ac0da3c0938b8e0bca

Source: git://sourceware.org/git/dwz.git?obj=%{dwz_branch}/%{dwz_commit}&export=dwz-%{dwz_commit}&output=/dwz-%{dwz_commit}.tgz

%prep
%setup -T -b 0 -n dwz-%{dwz_commit}

%build
make %{makeprocesses}

%install
mkdir -p %{i}/bin
cp dwz %{i}/bin
