### RPM cms cms_oracleocci_abi_hack-fake 20180210
%define tag 88b2a965305226df1822a14af8fe7174ee5f1614
Source: git+https://github.com/cms-sw/cms_oracleocci_abi_hack.git?obj=master/%{tag}&export=%{n}-%{realversion}&output=/%{n}-%{realversion}.tgz
Requires: oracle-fake
BuildRequires: gmake

%prep
%setup -n %{n}-%{realversion}

%build
export INCLUDE_DIR=${ORACLE_FAKE_ROOT}/include
export LIB_DIR=${ORACLE_FAKE_ROOT}/lib
make %{makeprocesses}

%install
[ -d  build/lib ] && cp -r build/lib %{i}/lib
cp -r build/include %{i}/include
# bla bla
