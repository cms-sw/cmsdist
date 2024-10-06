### RPM external dwz 0.15
Requires: xxhash
%define dwz_branch master
%define dwz_commit 0171f3e7ac09fa44cb1eb299f2703faa113a207e

Source: git://sourceware.org/git/dwz.git?obj=%{dwz_branch}/%{dwz_commit}&export=dwz-%{dwz_commit}&output=/dwz-%{dwz_commit}.tgz

%prep
%setup -T -b 0 -n dwz-%{dwz_commit}

%build
make %{makeprocesses} \
  CFLAGS="-I${XXHASH_ROOT}/include -O2" \
  LDFLAGS="-L${XXHASH_ROOT}/lib"

%install
mkdir -p %{i}/bin
cp dwz %{i}/bin
