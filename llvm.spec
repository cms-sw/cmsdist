### RPM external llvm 4.0.0
## INITENV +PATH LD_LIBRARY_PATH %{i}/lib64
## INITENV +PATH PYTHONPATH %{i}/lib64/python$(echo $PYTHON_VERSION | cut -d. -f 1,2)/site-packages

BuildRequires: python cmake ninja
Requires: gcc zlib

%define llvmCommit 6f0da3f936d586b289d15eac1c72b6a0141aa461
%define llvmBranch cms/6f0da3f
%define clangCommit bd48c3989247f27f75ca5f68ea7a504daf43397e
%define clangBranch cms/b3eb023
%define clangToolsExtraCommit 25e8e1682d1d2b76ee38eb23954e2c94513895d3
%define clangToolsExtraBranch cms/25e8e16
%define compilerRtCommit 99cc7eae4446047c6c17f456f24e49dd65067d4e
%define compilerRtBranch cms/99cc7ea
%define openmpCommit 7ca47d5c846d6d152b4c35589604f452ccd634e3
%define openmpBranch cms/7ca47d5
%define iwyuCommit eb7f5d1ef02836575aebfe5a95977f067064cee2
%define iwyuBranch cms/eb7f5d1
%define lldCommit bd6ea5cfe76b936f29b8a65d38ae47bb6ac02327
%define lldBranch cms/bd6ea5c
Source0: git+https://github.com/cms-externals/llvm.git?obj=%{llvmBranch}/%{llvmCommit}&export=llvm-%{realversion}-%{llvmCommit}&module=llvm-%realversion-%llvmCommit&output=/llvm-%{realversion}-%{llvmCommit}.tgz
Source1: git+https://github.com/cms-externals/clang.git?obj=%{clangBranch}/%{clangCommit}&export=clang-%{realversion}-%{clangCommit}&module=clang-%realversion-%clangCommit&output=/clang-%{realversion}-%{clangCommit}.tgz
Source2: git+https://github.com/cms-externals/clang-tools-extra.git?obj=%{clangToolsExtraBranch}/%{clangToolsExtraCommit}&export=clang-tools-extra-%{realversion}-%{clangToolsExtraCommit}&module=clang-tools-extra-%{realversion}-%{clangToolsExtraCommit}&output=/clang-tools-extra-%{realversion}-%{clangToolsExtraCommit}.tgz
Source3: git+https://github.com/cms-externals/compiler-rt.git?obj=%{compilerRtBranch}/%{compilerRtCommit}&export=compiler-rt-%{realversion}-%{compilerRtCommit}&module=compiler-rt-%{realversion}-%{compilerRtCommit}&output=/compiler-rt-%{realversion}-%{compilerRtCommit}.tgz
Source4: git+https://github.com/cms-externals/openmp.git?obj=%{openmpBranch}/%{openmpCommit}&export=openmp-%{realversion}-%{openmpCommit}&module=openmp-%{realversion}-%{openmpCommit}&output=/openmp-%{realversion}-%{openmpCommit}.tgz
Source5: git+https://github.com/cms-externals/include-what-you-use.git?obj=%{iwyuBranch}/%{iwyuCommit}&export=iwyu-%{realversion}-%{iwyuCommit}&module=iwyu-%{realversion}-%{iwyuCommit}&output=/iwyu-%{realversion}-%{iwyuCommit}.tgz
Source6: git+https://github.com/cms-externals/lld.git?obj=%{lldBranch}/%{lldCommit}&export=lld-%{realversion}-%{lldCommit}&module=lld-%{realversion}-%{lldCommit}&output=/lld-%{realversion}-%{lldCommit}.tgz

%define keep_archives true

%prep
%setup -T -b0 -n llvm-%realversion-%llvmCommit
%setup -T -D -a1 -c -n llvm-%realversion-%llvmCommit/tools
mv clang-%realversion-%clangCommit clang
%setup -T -D -a6 -c -n llvm-%{realversion}-%{llvmCommit}/tools
mv lld-%{realversion}-%{lldCommit} lld
%setup -T -D -a2 -c -n llvm-%{realversion}-%{llvmCommit}/tools/clang/tools
mv clang-tools-extra-%{realversion}-%{clangToolsExtraCommit} extra
%setup -T -D -a5 -c -n llvm-%{realversion}-%{llvmCommit}/tools/clang/tools
mv iwyu-%{realversion}-%{iwyuCommit} include-what-you-use
%setup -T -D -a3 -c -n llvm-%{realversion}-%{llvmCommit}/projects
mv compiler-rt-%{realversion}-%{compilerRtCommit} compiler-rt
%setup -T -D -a4 -c -n llvm-%{realversion}-%{llvmCommit}/projects
mv openmp-%{realversion}-%{openmpCommit} openmp
%setup -T -D -n llvm-%realversion-%llvmCommit

# include-what-you-see is not LLVM project, we have to
# add it explicitly.
sed -ibak '/add_clang_subdirectory(libclang)/a add_subdirectory(include-what-you-use)' tools/clang/tools/CMakeLists.txt

%build
rm -rf %{_builddir}/build
mkdir -p %{_builddir}/build
cd %{_builddir}/build

cmake %{_builddir}/llvm-%{realversion}-%{llvmCommit} \
  -G Ninja \
  -DCMAKE_INSTALL_PREFIX:PATH="%{i}" \
  -DCMAKE_BUILD_TYPE:STRING=Release \
  -DLLVM_LIBDIR_SUFFIX:STRING=64 \
  -DLLVM_BINUTILS_INCDIR:STRING="${GCC_ROOT}/include" \
  -DBUILD_SHARED_LIBS:BOOL=ON \
  -DLLVM_ENABLE_EH:BOOL=ON \
  -DLLVM_ENABLE_PIC:BOOL=ON \
  -DLLVM_ENABLE_RTTI:BOOL=ON \
  -DLLVM_TARGETS_TO_BUILD:STRING="X86;PowerPC;AArch64" \
  -DCMAKE_REQUIRED_INCLUDES="${ZLIB_ROOT}/include" \
  -DCMAKE_PREFIX_PATH="${ZLIB_ROOT}"

ninja -v %{makeprocesses} -l $(getconf _NPROCESSORS_ONLN)

%install
cd ../build
ninja -v %{makeprocesses} -l $(getconf _NPROCESSORS_ONLN) install

BINDINGS_PATH=%{i}/lib64/python$(echo $PYTHON_VERSION | cut -d. -f 1,2)/site-packages
mkdir -p $BINDINGS_PATH
cp -r %{_builddir}/llvm-%{realversion}-%{llvmCommit}/tools/clang/bindings/python/clang $BINDINGS_PATH

rm -f %{_builddir}/llvm-%{realversion}-%{llvmCommit}/tools/clang/tools/scan-build/set-xcode*
find %{_builddir}/llvm-%{realversion}-%{llvmCommit}/tools/clang/tools/scan-build -exec install {} %{i}/bin \;
find %{_builddir}/llvm-%{realversion}-%{llvmCommit}/tools/clang/tools/scan-view -type f -exec install {} %{i}/bin \;
# Remove compiled AppleScript scripts, otherwise install_name_tool from
# DEFAULT_INSTALL_POSTAMBLE will fail. These are non-object files.
# TODO: Improve DEFAULT_INSTALL_POSTAMBLE for OS X.
rm -f %{i}/bin/FileRadar.scpt %{i}/bin/GetRadarVersion.scpt

# Avoid dependency on /usr/bin/python, Darwin + Xcode specific
rm -f %{i}/bin/set-xcode-analyzer

%post
%{relocateConfig}include/llvm/Config/llvm-config.h
