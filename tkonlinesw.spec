### RPM external tkonlinesw 1.2
Source: afs:///afs/cern.ch/cms/external/TkOnlineSw/%{v}/slc3_ia32_gcc323?export=/%{n}-%{v}.slc3_ia32_gcc323.tar.gz
Source1: afs:///afs/cern.ch/cms/external/TkOnlineSw/%{v}/slc4_ia32_gcc345?export=/%{n}-%{v}.slc4_ia32_gcc345.tar.gz
Requires: xerces-c
%prep
rm -rf ./*
%if "%cmsplatf" == "slc3_ia32_gcc323"
tar xzvf %_sourcedir/%{n}-%{v}.slc3_ia32_gcc323.tar.gz
%endif

%if "%cmsplatf" == "slc4_ia32_gcc345"
tar xzvf %_sourcedir/%{n}-%{v}.slc4_ia32_gcc345.tar.gz
%endif

# This is a kludge around a kludge...
%if "%cmsplatf" == "slc4_amd64_gcc345"
tar xzvf %_sourcedir/%{n}-%{v}.slc4_ia32_gcc345.tar.gz
%endif

%build
%install
mkdir -p %i/include
mkdir -p %i/lib
cp -r lib/* %i/lib
cp -r include/* %i/include
