### RPM external llvm 3.3
## INITENV +PATH LD_LIBRARY_PATH %i/lib64

BuildRequires: python

Requires: gcc

%define llvmRevision 183501
%define clangRevision 183502
%define llvmBranch %(echo %realversion | sed -e 's|[.]||')
# s/#/S/ to use the official version.
Source0: svn://llvm.org/svn/llvm-project/llvm/branches/release_%llvmBranch/?scheme=http&revision=%llvmRevision&module=llvm-%realversion-%llvmRevision&output=/llvm-%realversion-%llvmRevision.tgz
Source1: svn://llvm.org/svn/llvm-project/cfe/branches/release_%llvmBranch/?scheme=http&revision=%clangRevision&module=clang-%realversion-%clangRevision&output=/clang-%realversion-%clangRevision.tgz
# SVN builds. Comment out to use the official version.
#Source0: svn://llvm.org/svn/llvm-project/llvm/trunk/?scheme=http&revision=%llvmRevision&module=llvm-%realversion-%llvmRevision&output=/llvm-%realversion-%llvmRevision.tgz
#Source1: svn://llvm.org/svn/llvm-project/cfe/trunk/?scheme=http&revision=%clangRevision&module=clang-%realversion-%clangRevision&output=/clang-%realversion-%clangRevision.tgz
Patch0: llvm-3.1-fix-requires
Patch1: llvm-3.2-getGCCToolchainDir
Patch2: llvm-3.3-add-triplet-x86_64-redhat-linux-gnu
Patch3: llvm-3.3-cms-custom-cxx11-attrs
%define keep_archives true

%prep
%setup -T -b0 -n llvm-%realversion-%llvmRevision
%setup -T -D -a1 -c -n llvm-%realversion-%llvmRevision/tools
mv clang-%realversion-%clangRevision clang
cd clang
%patch0 -p1
%patch1 -p1
%patch2 -p1
%patch3 -p1
%setup -T -D -n llvm-%realversion-%llvmRevision

%build

CONF_OPTS=
case "%{cmsplatf}" in
  slc*|fc*)
    CONF_OPTS="${CONF_OPTS} --with-binutils-include=${GCC_ROOT}/include"
    ;;
esac

mkdir objs ; cd objs
../configure --prefix=%i --enable-optimized ${CONF_OPTS}
make %makeprocesses

%install
cd objs
make install
rm -f ../tools/clang/tools/scan-build/set-xcode*
find ../tools/clang/tools/scan-build -exec install {} %i/bin \;
find ../tools/clang/tools/scan-view -type f -exec install {} %i/bin \;
# Remove compiled AppleScript scripts, otherwise install_name_tool from
# DEFAULT_INSTALL_POSTAMBLE will fail. These are non-object files.
# TODO: Improve DEFAULT_INSTALL_POSTAMBLE for OS X.
rm  %i/bin/FileRadar.scpt %i/bin/GetRadarVersion.scpt
# Fix up a perl path
perl -p -i -e 's|^#!.*perl(.*)|#!/usr/bin/env perl$1|' %i/bin/llvm-config

%post
%{relocateConfig}include/llvm/Config/config.h
%{relocateConfig}include/llvm/Config/llvm-config.h
%{relocateConfig}include/clang/Config/config.h
