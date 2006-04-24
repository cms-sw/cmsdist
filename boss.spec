### RPM cms boss 3.6.3
## INITENV +PATH PATH %i/bin
%define downloadv %(echo v%v | tr '.' '_')
Source: http://boss.bo.infn.it/%n-%downloadv.tar.gz
Requires: uuid
%prep
%setup -n %n-%downloadv
%build
# BOSS does not support separate build and install directory... Building
# directly in %i.
mkdir -p %i
cp -r ./* %{i}
cd %{i}
make
%install
