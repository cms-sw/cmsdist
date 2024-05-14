### RPM external mozsearch 20240514

%define tag d697005b97f28d493a24887ed25fd2e68839c716
%define branch master

%define github_user mozsearch
Source: git+https://github.com/%{github_user}/%{n}.git?obj=%{branch}/%{tag}&export=%{n}-%{realversion}&output=/%{n}-%{realversion}-%{tag}.tgz
Patch0: mozsearch-gcc-toolchain
BuildRequires: gmake
Requires: llvm

%prep
%setup -n %{n}-%{realversion}
%patch0 -p1

%build
cd clang-plugin
GCC_ROOT=${GCC_ROOT} make %{makeprocesses} build 

%install
mkdir -p %{i}/lib64
cp clang-plugin/libclang-index-plugin.so %{i}/lib64
