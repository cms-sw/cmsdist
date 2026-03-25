### RPM external llvm 21.1.4
## INITENV +PATH LD_LIBRARY_PATH %{i}/lib64
## INITENV +PATH PYTHON3PATH %{i}/lib64/python%{cms_python3_major_minor_version}/site-packages

BuildRequires: cmake cms-ninja
Requires: gcc zlib python3 libxml2 zstd libunwind
%{!?without_cuda:Requires: cuda}

%define llvmCommit 3063d23cfa249166b2e0c33a02c7300c20ffb2d
%define llvmBranch cms/llvmorg-21.1.4
%define iwyuCommit 791e69ea4662cb3e74e8128fd5fd69bd7f4ea6b3
%define iwyuBranch clang_21

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
# defines omptarget_cuda_archs

rm -rf %{_builddir}/build
mkdir -p %{_builddir}/build
cd %{_builddir}/build

host_triple=$(gcc -dumpmachine)
cmake %{_builddir}/llvm-%{realversion}-%{llvmCommit}/llvm \
  -G Ninja \
%if 0%{!?use_system_gcc:1}
  -DLLVM_BINUTILS_INCDIR:STRING="${GCC_ROOT}/include" \
%endif
  -DLLVM_ENABLE_PROJECTS="clang;clang-tools-extra;mlir;lld" \
  -DLLVM_ENABLE_RUNTIMES="libcxx;libcxxabi;libunwind;compiler-rt;openmp" \
  -DIWYU_RESOURCE_RELATIVE_TO="iwyu" \
  -DCMAKE_INSTALL_PREFIX:PATH="%{i}" \
  -DCMAKE_BUILD_TYPE:STRING=Release \
  -DLLVM_INSTALL_UTILS=ON \
  -DLLVM_LIBDIR_SUFFIX:STRING=64 \
  -DLLVM_BUILD_LLVM_DYLIB:BOOL=ON \
  -DLLVM_LINK_LLVM_DYLIB:BOOL=ON \
  -DLLVM_ENABLE_EH:BOOL=ON \
  -DLLVM_ENABLE_PIC:BOOL=ON \
  -DLLVM_ENABLE_RTTI:BOOL=ON \
  -DCOMPILER_RT_INCLUDE_TESTS=OFF \
  -DLLVM_INCLUDE_TESTS=OFF \
  -DLLVM_HOST_TRIPLE=${host_triple} \
  -DLLVM_TARGETS_TO_BUILD:STRING="X86;PowerPC;AArch64;RISCV;NVPTX" \
%if 0%{!?without_cuda:1}
  -DLIBOMPTARGET_NVPTX_ALTERNATE_HOST_COMPILER=/usr/bin/gcc \
  -DLIBOMPTARGET_NVPTX_COMPUTE_CAPABILITIES="%omptarget_cuda_archs" \
%endif
  -DCMAKE_REQUIRED_INCLUDES="${ZLIB_ROOT}/include" \
  -DCMAKE_PREFIX_PATH="${ZLIB_ROOT};${LIBXML2_ROOT};${ZSTD_ROOT};${LIBUNWIND_ROOT}"

%if 0%{!?use_system_gcc:1}
echo -e "--gcc-toolchain=$GCC_ROOT\n--target=$host_triple" > bin/clang++.cfg
ln -s clang++.cfg bin/clang.cfg
%endif

ninja -v %{makeprocesses}
bin/clang-tidy --checks=* --list-checks | grep cms-handle

%install
cd ../build
ninja -v %{makeprocesses} install

#Create libomp symlink
host_triple=$(gcc -dumpmachine)
ln -s ${host_triple}/libomp.so %{i}/lib64/libomp.so

# Install clang python bindings
BINDINGS_PATH=%{i}/lib64/python%{cms_python3_major_minor_version}/site-packages
DISTINFO_DIR=${BINDINGS_PATH}/libclang-%{realversion}.dist-info
mkdir -p ${DISTINFO_DIR}
cp -r %{_builddir}/llvm-%{realversion}-%{llvmCommit}/clang/bindings/python/clang ${BINDINGS_PATH}
cat > ${DISTINFO_DIR}/METADATA <<EOF
Metadata-Version: 2.1
Name: libclang
Version: %{realversion}
Summary: Python bindings for libclang
EOF

rm -f %{_builddir}/llvm-%{realversion}-%{llvmCommit}/clang/tools/scan-build/set-xcode*
find %{_builddir}/llvm-%{realversion}-%{llvmCommit}/clang/tools/scan-build -exec install {} %{i}/bin \;
find %{_builddir}/llvm-%{realversion}-%{llvmCommit}/clang/tools/scan-view -type f -exec install {} %{i}/bin \;
# Remove compiled AppleScript scripts, otherwise install_name_tool from
# DEFAULT_INSTALL_POSTAMBLE will fail. These are non-object files.
# TODO: Improve DEFAULT_INSTALL_POSTAMBLE for OS X.
rm -f %{i}/bin/FileRadar.scpt %{i}/bin/GetRadarVersion.scpt

# Avoid dependency on /usr/bin/python, Darwin + Xcode specific
rm -f %{i}/bin/set-xcode-analyzer

#Copy clang configuration
mv bin/clang++.cfg %{i}/bin
mv bin/clang.cfg %{i}/bin

%post
%{relocateConfig}include/llvm/Config/llvm-config.h
%{relocateConfig}include/clang/Config/config.h
%{relocateConfig}lib64/cmake/llvm/LLVMConfig.cmake
%if 0%{!?use_system_gcc:1}
%{relocateConfig}bin/clang++.cfg
%endif
