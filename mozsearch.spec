### RPM external mozsearch 20251022

%define tag 1c886cc95c4e811709e97f711d7691ff8b87bda9
%define branch master

%define github_user mozsearch
Source: git+https://github.com/%{github_user}/%{n}.git?obj=%{branch}/%{tag}&export=%{n}-%{realversion}&output=/%{n}-%{realversion}-%{tag}.tgz
Patch0: mozsearch-gcc-toolchain
Patch1: mozsearch-clang21
BuildRequires: gmake
Requires: llvm

%prep
%setup -n %{n}-%{realversion}
%patch0 -p1
%patch1 -p1

%build
cd clang-plugin
GCC_ROOT=${GCC_ROOT} make %{makeprocesses} build 

%install
mkdir -p %{i}/lib64
cp clang-plugin/libclang-index-plugin.so %{i}/lib64
