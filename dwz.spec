### RPM external dwz 0.16
Requires: xxhash

Source: https://cmsrep.cern.ch/cmssw/download/dwz-%{realversion}.tar.gz

%prep
%setup -T -b 0 -n dwz

%build
make %{makeprocesses} \
  CFLAGS="-I${XXHASH_ROOT}/include -O2" \
  LDFLAGS="-L${XXHASH_ROOT}/lib"

%install
mkdir -p %{i}/bin
cp dwz %{i}/bin
