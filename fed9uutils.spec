### RPM external fed9uutils 2.4.1
%define downloadv %(echo %v | cut -d. -f 1,2)
Source: afs:///afs/cern.ch/cms/external/Fed9UUtils/?export=/%{n}-%{v}.tar.gz
Provides: libxerces-c.so.23
%build
%install
mkdir -p %i/include
mkdir -p %i/lib
cp -r  libFed9UUtils.so %i/lib
cp -r include/* %i/include
