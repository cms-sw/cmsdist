### RPM external tkonlinesw 1.1
Source: afs:///afs/cern.ch/cms/external/TkOnlineSw/1.1/slc3_ia32_gcc323?export=/%{n}-%{v}.tar.gz
%build
%install
mkdir -p %i/include
mkdir -p %i/lib
cp -r lib/* %i/lib
cp -r include/* %i/include
