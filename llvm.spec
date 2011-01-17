### RPM external llvm 2.8
## NOCOMPILER
## INITENV +PATH LD_LIBRARY_PATH %i/lib64

Source0: http://llvm.org/releases/%realversion/llvm-%realversion.tgz
Source1: http://llvm.org/releases/%realversion/clang-%realversion.tgz 

%prep
%setup -T -b0 -n llvm-%realversion
%setup -T -D -a1 -c -n llvm-%realversion/tools
mv clang-%realversion clang
%setup -T -D -n llvm-%realversion
pwd

%build
pwd
mkdir objs ; cd objs
../configure --prefix=%i --enable-optimized
make %makeprocesses

%install
cd objs
make install
# Fix up a perl path
perl -p -i -e 's|^#!.*perl(.*)|#!/usr/bin/env perl$1|' %i/bin/llvm-config
