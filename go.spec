### RPM external go 1.25.5
BuildRequires: go-bootstrap
AutoReqProv: no
Source: https://go.dev/dl/go%{realversion}.src.tar.gz

%prep
%setup -n go

%build
cd src
export GOROOT_BOOTSTRAP=${GO_BOOTSTRAP_ROOT}
./make.bash

%install
rsync -a ./ %i/
