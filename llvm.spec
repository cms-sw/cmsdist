### RPM external llvm 3.7.1
## INITENV +PATH LD_LIBRARY_PATH %{i}/lib64
## INITENV +PATH PYTHONPATH %{i}/lib64/python$(echo $PYTHON_VERSION | cut -d. -f 1,2)/site-packages

BuildRequires: python cmake ninja
Requires: gcc zlib

%define llvmCommit 33c352b3eda89abc24e7511d9045fa2e499a42e3
%define llvmBranch cms/33c352b
%define clangCommit 86f9ed77080392c73d23c1c2c103c926ebb0e14a
%define clangBranch cms/0dbefa1
%define clangToolsExtraCommit 17700095a2b35fc7d7699afe5a6ba1961389fd59
%define clangToolsExtraBranch cms/1770009
%define compilerRtCommit b5214093d4c91ed5352d35ee9126665fabfa97fe
%define compilerRtBranch cms/b521409
%define openmpCommit bc10909fa897a985c5f346b47a88f65b920efba1
%define openmpBranch cms/bc10909
Source0: git+https://github.com/cms-externals/llvm.git?obj=%{llvmBranch}/%{llvmCommit}&export=llvm-%{realversion}-%{llvmCommit}&module=llvm-%realversion-%llvmCommit&output=/llvm-%{realversion}-%{llvmCommit}.tgz
Source1: git+https://github.com/cms-externals/clang.git?obj=%{clangBranch}/%{clangCommit}&export=clang-%{realversion}-%{clangCommit}&module=clang-%realversion-%clangCommit&output=/clang-%{realversion}-%{clangCommit}.tgz
Source2: git+https://github.com/cms-externals/clang-tools-extra.git?obj=%{clangToolsExtraBranch}/%{clangToolsExtraCommit}&export=clang-tools-extra-%{realversion}-%{clangToolsExtraCommit}&module=clang-tools-extra-%{realversion}-%{clangToolsExtraCommit}&output=/clang-tools-extra-%{realversion}-%{clangToolsExtraCommit}.tgz
Source3: git+https://github.com/cms-externals/compiler-rt.git?obj=%{compilerRtBranch}/%{compilerRtCommit}&export=compiler-rt-%{realversion}-%{compilerRtCommit}&module=compiler-rt-%{realversion}-%{compilerRtCommit}&output=/compiler-rt-%{realversion}-%{compilerRtCommit}.tgz
Source4: git+https://github.com/cms-externals/openmp.git?obj=%{openmpBranch}/%{openmpCommit}&export=openmp-%{realversion}-%{openmpCommit}&module=openmp-%{realversion}-%{openmpCommit}&output=/openmp-%{realversion}-%{openmpCommit}.tgz

# Still need forward porting.
%define keep_archives true

%prep
%setup -T -b0 -n llvm-%realversion-%llvmCommit
%setup -T -D -a1 -c -n llvm-%realversion-%llvmCommit/tools
mv clang-%realversion-%clangCommit clang
%setup -T -D -a2 -c -n llvm-%{realversion}-%{llvmCommit}/tools/clang/tools
mv clang-tools-extra-%{realversion}-%{clangToolsExtraCommit} extra
%setup -T -D -a3 -c -n llvm-%{realversion}-%{llvmCommit}/projects
mv compiler-rt-%{realversion}-%{compilerRtCommit} compiler-rt
%setup -T -D -a4 -c -n llvm-%{realversion}-%{llvmCommit}/projects
mv openmp-%{realversion}-%{openmpCommit} openmp
%setup -T -D -n llvm-%realversion-%llvmCommit

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

%post
%{relocateConfig}include/llvm/Config/llvm-config.h
