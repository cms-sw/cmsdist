### RPM external llvm 3.6
## INITENV +PATH LD_LIBRARY_PATH %i/lib64

BuildRequires: python
Requires: gcc

%define llvmCommit f04ce0e65747b16e6f321c0fdd38b6e1dc3271a3
%define llvmBranch cms/f04ce0e
%define clangCommit 3643e3a97ed4124eaf1322921cd0241fbd84b0c6
%define clangBranch cms/65d8b4c
%define clangToolsExtraCommit 13f3e9fac71230b24857613d683fa146ef0da7a8
%define clangToolsExtraBranch cms/13f3e9f
Source0: git+https://github.com/cms-externals/llvm.git?obj=%{llvmBranch}/%{llvmCommit}&export=llvm-%{realversion}-%{llvmCommit}&module=llvm-%realversion-%llvmCommit&output=/llvm-%{realversion}-%{llvmCommit}.tgz
Source1: git+https://github.com/cms-externals/clang.git?obj=%{clangBranch}/%{clangCommit}&export=clang-%{realversion}-%{clangCommit}&module=clang-%realversion-%clangCommit&output=/clang-%{realversion}-%{clangCommit}.tgz
Source2: git+https://github.com/cms-externals/clang-tools-extra.git?obj=%{clangToolsExtraBranch}/%{clangToolsExtraCommit}&export=clang-tools-extra-%{realversion}-%{clangToolsExtraCommit}&module=clang-tools-extra-%{realversion}-%{clangToolsExtraCommit}&output=/clang-tools-extra-%{realversion}-%{clangToolsExtraCommit}.tgz

# Still need forward porting.
%define keep_archives true

%prep
%setup -T -b0 -n llvm-%realversion-%llvmCommit
%setup -T -D -a1 -c -n llvm-%realversion-%llvmCommit/tools
mv clang-%realversion-%clangCommit clang
%setup -T -D -a2 -c -n llvm-%{realversion}-%{llvmCommit}/tools/clang/tools
mv clang-tools-extra-%{realversion}-%{clangToolsExtraCommit} extra
%setup -T -D -n llvm-%realversion-%llvmCommit

%build

CONF_OPTS=
case "%{cmsplatf}" in
  slc*|fc*)
    CONF_OPTS="${CONF_OPTS} --with-binutils-include=${GCC_ROOT}/include"
    ;;
esac

mkdir objs ; cd objs
../configure --prefix=%i --enable-optimized ${CONF_OPTS} \
             --disable-terminfo --enable-bindings=none \
             CC="gcc" CXX="g++" CPP="gcc -E" CXXCPP="g++ -E"
make %makeprocesses

%install
cd objs
make install

BINDINGS_PATH=%i/lib/python$(echo $PYTHON_VERSION | cut -d. -f 1,2)/site-packages
mkdir -p $BINDINGS_PATH
cp -r ../tools/clang/bindings/python/clang $BINDINGS_PATH

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
