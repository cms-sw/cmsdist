### RPM external llvm 16.0.3
## INITENV +PATH LD_LIBRARY_PATH %{i}/lib64
## INITENV +PATH PYTHON3PATH %{i}/lib64/python%{cms_python3_major_minor_version}/site-packages

BuildRequires: cmake ninja
Requires: gcc zlib python3
Requires: cuda
AutoReq: no

%define llvmCommit bd1b99af77c08abf7a677e2ae688e57afd0f922f
%define llvmBranch cms/release/16.x/464bda7
%define iwyuCommit 14e9b208914a84fcdf49bf9f5d08897a4b3dc4b8
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
  -DGCC_INSTALL_PREFIX="${GCC_ROOT}" \
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
  -DLLVM_HOST_TRIPLE=$(gcc -dumpmachine) \
  -DLLVM_TARGETS_TO_BUILD:STRING="X86;PowerPC;AArch64;NVPTX" \
  -DLIBOMPTARGET_NVPTX_ALTERNATE_HOST_COMPILER=/usr/bin/gcc \
  -DLIBOMPTARGET_NVPTX_COMPUTE_CAPABILITIES="%llvm_cuda_arch" \
  -DCMAKE_REQUIRED_INCLUDES="${ZLIB_ROOT}/include" \
  -DCMAKE_PREFIX_PATH="${ZLIB_ROOT}"

ninja -v %{makeprocesses}
ninja -v %{makeprocesses} check-clang-tools
bin/clang-tidy --checks=* --list-checks | grep cms-handle

%install
cd ../build
ninja -v %{makeprocesses} install

BINDINGS_PATH=%{i}/lib64/python%{cms_python3_major_minor_version}/site-packages
PKG_INFO_FILE=$BINDINGS_PATH/clang-%{realversion}-py%{cms_python3_major_minor_version}.egg-info/PKG-INFO
mkdir -p $BINDINGS_PATH
cp -r %{_builddir}/llvm-%{realversion}-%{llvmCommit}/clang/bindings/python/clang $BINDINGS_PATH
mkdir $BINDINGS_PATH/clang-%{realversion}-py%{cms_python3_major_minor_version}.egg-info
echo -e "Metadata-Version: 1.1\nName: clang\nVersion: %{realversion}" > ${PKG_INFO_FILE}

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
%{relocateConfig}include/clang/Config/config.h
%{relocateConfig}lib64/cmake/llvm/LLVMConfig.cmake
