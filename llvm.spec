### RPM external llvm 7.0.0
## INITENV +PATH LD_LIBRARY_PATH %{i}/lib64
## INITENV +PATH PYTHON27PATH %{i}/lib64/python`echo $PYTHON_VERSION | cut -d. -f 1,2`/site-packages
%define isamd64 %(case %{cmsplatf} in (*_amd64_*) echo 1 ;; (*) echo 0 ;; esac)

BuildRequires: python cmake ninja
Requires: gcc zlib
%if %{isamd64}
Requires: cuda
%endif
AutoReq: no

%define llvmCommit ff0a5e8a591ed8bfc14320740863b357b1774f49
%define llvmBranch cms/release_70/342187
%define iwyuCommit 7b8980310f98ea76ac6d4e703d8bd07bde3d8ebc
%define iwyuBranch master

Source0: git+https://github.com/cms-externals/llvm-project-20170507.git?obj=%{llvmBranch}/%{llvmCommit}&export=llvm-%{realversion}-%{llvmCommit}&module=llvm-%{realversion}-%{llvmCommit}&output=/llvm-%{realversion}-%{llvmCommit}.tgz
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
