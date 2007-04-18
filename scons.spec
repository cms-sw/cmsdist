### RPM external scons 0.96.1
Requires: gcc-wrapper
Source: http://eulisse.web.cern.ch/eulisse/%n-%v.tar.gz

%build
## IMPORT gcc-wrapper
%install
cp -r ./* %i
