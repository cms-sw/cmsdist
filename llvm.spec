### RPM external llvm 3.2
## INITENV +PATH LD_LIBRARY_PATH %i/lib64
%define llvmRevision 157628
%define clangRevision 157628
%define llvmBranch %(echo %realversion | sed -e 's|[.]||')
# s/#/S/ to use the official version.
#Source0: svn://llvm.org/svn/llvm-project/llvm/branches/release_%llvmBranch/?scheme=http&revision=%llvmRevision&module=llvm-%realversion-%llvmRevision&output=/llvm-%realversion-%llvmRevision.tgz
#Source1: svn://llvm.org/svn/llvm-project/cfe/branches/release_%llvmBranch/?scheme=http&revision=%clangRevision&module=clang-%realversion-%clangRevision&output=/clang-%realversion-%clangRevision.tgz
# SVN builds. Comment out to use the official version.
Source0: svn://llvm.org/svn/llvm-project/llvm/trunk/?scheme=http&revision=%llvmRevision&module=llvm-%realversion-%llvmRevision&output=/llvm-%realversion-%llvmRevision.tgz
Source1: svn://llvm.org/svn/llvm-project/cfe/trunk/?scheme=http&revision=%clangRevision&module=clang-%realversion-%clangRevision&output=/clang-%realversion-%clangRevision.tgz
Patch0: llvm-3.1-custom-gcc
Patch1: llvm-3.1-fix-requires
%define keep_archives true

%prep
%setup -T -b0 -n llvm-%realversion-%llvmRevision
%setup -T -D -a1 -c -n llvm-%realversion-%llvmRevision/tools
mv clang-%realversion-%clangRevision clang
cd clang
%patch0 -p1
%patch1 -p1
%setup -T -D -n llvm-%realversion-%llvmRevision

%build
mkdir objs ; cd objs
../configure --prefix=%i --enable-optimized
make %makeprocesses

%install
cd objs
make install
rm -f ../tools/clang/tools/scan-build/set-xcode*
find ../tools/clang/tools/scan-build -exec install {} %i/bin \;
find ../tools/clang/tools/scan-view -type f -exec install {} %i/bin \;
# Fix up a perl path
perl -p -i -e 's|^#!.*perl(.*)|#!/usr/bin/env perl$1|' %i/bin/llvm-config
