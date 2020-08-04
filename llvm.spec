### RPM external llvm 10.0.0
## INITENV +PATH LD_LIBRARY_PATH %{i}/lib64
## INITENV +PATH PYTHON27PATH %{i}/lib64/python`echo $PYTHON_VERSION | cut -d. -f 1,2`/site-packages
## INITENV +PATH PYTHON3PATH %{i}/lib64/python`echo $PYTHON3_VERSION | cut -d. -f 1,2`/site-packages

BuildRequires: cmake ninja
Requires: gcc zlib python python3
Requires: cuda
AutoReq: no

%define llvmCommit 4b3acf7d70558fefca729efe381e3900da4591dd
%define llvmBranch cms/release/10.x/92d5c1b
%define iwyuCommit a5a6f27dabeb7fbc59b06ea949a312201c2fbdcf
%define iwyuBranch master

Source0: git+https://github.com/cms-externals/llvm-project.git?obj=%{llvmBranch}/%{llvmCommit}&export=llvm-%{realversion}-%{llvmCommit}&module=llvm-%{realversion}-%{llvmCommit}&output=/llvm-%{realversion}-%{llvmCommit}.tgz
Source1: git+https://github.com/include-what-you-use/include-what-you-use.git?obj=%{iwyuBranch}/%{iwyuCommit}&export=iwyu-%{realversion}-%{iwyuCommit}&module=iwyu-%{realversion}-%{iwyuCommit}&output=/iwyu-%{realversion}-%{iwyuCommit}.tgz

%define keep_archives true

%prep
%setup -T -b0 -n llvm-%{realversion}-%{llvmCommit}

# include-what-you-see is not LLVM project, we add it explicitly to the clang tools
%setup -T -D -a1 -c -n llvm-%{realversion}-%{llvmCommit}/clang/tools
mv iwyu-%{realversion}-%{iwyuCommit} include-what-you-use
sed -ibak '/add_clang_subdirectory(libclang)/a add_subdirectory(include-what-you-use)' CMakeLists.txt

# move back to the main setup directory
%setup -T -D -n llvm-%{realversion}-%{llvmCommit}

%build
## INCLUDE cuda-flags
# defines llvm_cuda_arch

rm -rf %{_builddir}/build
mkdir -p %{_builddir}/build
cd %{_builddir}/build

cmake %{_builddir}/llvm-%{realversion}-%{llvmCommit}/llvm \
  -G Ninja \
  -DLLVM_ENABLE_PROJECTS="clang;clang-tools-extra;compiler-rt;lld;openmp" \
  -DCMAKE_INSTALL_PREFIX:PATH="%{i}" \
  -DCMAKE_BUILD_TYPE:STRING=Release \
  -DLLVM_LIBDIR_SUFFIX:STRING=64 \
  -DLLVM_BINUTILS_INCDIR:STRING="${GCC_ROOT}/include" \
  -DLLVM_BUILD_LLVM_DYLIB:BOOL=ON \
  -DLLVM_LINK_LLVM_DYLIB:BOOL=ON \
  -DLLVM_ENABLE_EH:BOOL=ON \
  -DLLVM_ENABLE_PIC:BOOL=ON \
  -DLLVM_ENABLE_RTTI:BOOL=ON \
  -DLLVM_TARGETS_TO_BUILD:STRING="X86;PowerPC;AArch64;NVPTX" \
  -DLIBOMPTARGET_NVPTX_ALTERNATE_HOST_COMPILER=/usr/bin/gcc \
  -DLIBOMPTARGET_NVPTX_COMPUTE_CAPABILITIES="%llvm_cuda_arch" \
  -DCMAKE_REQUIRED_INCLUDES="${ZLIB_ROOT}/include" \
  -DCMAKE_PREFIX_PATH="${ZLIB_ROOT}"

ninja -v %{makeprocesses} -l $(getconf _NPROCESSORS_ONLN)
ninja -v %{makeprocesses} -l $(getconf _NPROCESSORS_ONLN) check-clang-tools
bin/clang-tidy --checks=* --list-checks | grep cms-handle

%install
cd ../build
ninja -v %{makeprocesses} -l $(getconf _NPROCESSORS_ONLN) install

BINDINGS_PATH=%{i}/lib64/python$(echo $PYTHON_VERSION | cut -d. -f 1,2)/site-packages
mkdir -p $BINDINGS_PATH
cp -r %{_builddir}/llvm-%{realversion}-%{llvmCommit}/clang/bindings/python/clang $BINDINGS_PATH
BINDINGS_PATH=%{i}/lib64/python$(echo $PYTHON3_VERSION | cut -d. -f 1,2)/site-packages
mkdir -p $BINDINGS_PATH
cp -r %{_builddir}/llvm-%{realversion}-%{llvmCommit}/clang/bindings/python/clang $BINDINGS_PATH

rm -f %{_builddir}/llvm-%{realversion}-%{llvmCommit}/clang/tools/scan-build/set-xcode*
find %{_builddir}/llvm-%{realversion}-%{llvmCommit}/clang/tools/scan-build -exec install {} %{i}/bin \;
find %{_builddir}/llvm-%{realversion}-%{llvmCommit}/clang/tools/scan-view -type f -exec install {} %{i}/bin \;
# Remove compiled AppleScript scripts, otherwise install_name_tool from
# DEFAULT_INSTALL_POSTAMBLE will fail. These are non-object files.
# TODO: Improve DEFAULT_INSTALL_POSTAMBLE for OS X.
rm -f %{i}/bin/FileRadar.scpt %{i}/bin/GetRadarVersion.scpt

# Avoid dependency on /usr/bin/python, Darwin + Xcode specific
rm -f %{i}/bin/set-xcode-analyzer

%post
%{relocateConfig}include/llvm/Config/llvm-config.h
