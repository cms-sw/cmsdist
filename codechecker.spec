### RPM external codechecker 0.1
## INITENV +PATH LD_LIBRARY_PATH %i/lib64

%define tag d0f091c40569bf5b618f3e415a9b07fa6d9044fc
%define branch llvm10
%define github_user cms-externals
Source: git+https://github.com/%github_user/CMSCodeChecker.git?obj=%{branch}/%{tag}&export=%{n}-%{realversion}&output=/%{n}-%{realversion}.tgz

BuildRequires: cmake 
Requires: llvm

%prep
%setup -n %n-%{realversion}

%build
mkdir build
cd build

cmake ../ \
  -DCMAKE_INSTALL_PREFIX=%{i} \
  -DLLVM_DIR=${LLVM_ROOT}/lib64/llvm \
  -DClang_DIR=${LLVM_ROOT}/lib64/clang \
  -DCMAKE_BUILD_TYPE=Release \
  -DCMAKE_CXX_COMPILER=`which g++` \
  -DCMAKE_C_COMPILER=`which gcc` 

# Use makeprocess macro, it uses compiling_processes defined by
# build configuration file or build argument
make %makeprocesses VERBOSE=1

%install
cd build
make install
cd ..

%define strip_files %i/lib
%define keep_archives true

