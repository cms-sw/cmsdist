### RPM external icutils 2.4
Source: afs:///afs/cern.ch/cms/external/ICUtils?export=/%{n}-%{v}.tar.gz 
%build
%install
mkdir -p %i/lib
mkdir -p %i/include
cp libICUtils.so %i/lib
cp include/*.hh %i/include
