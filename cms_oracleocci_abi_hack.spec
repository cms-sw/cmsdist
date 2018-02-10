### RPM cms cms_oracleocci_abi_hack 20180209
%define tag 24d917b12c27a024d45859b86cb78699448f2eb4
Source: git+https://github.com/cms-sw/%{n}.git?obj=master/%{tag}&export=%{n}-%{realversion}&output=/%{n}-%{realversion}.tgz
Requires: oracle
BuildRequires: gmake

%define isdarwin %(case %{cmsos} in (osx*) echo 1 ;; (*) echo 0 ;; esac)
%define soext so
%if %isdarwin
%define soext dylib
%endif

%prep
%setup -n %{n}-%{realversion}

%build
export INCLUDE_DIR=${ORACLE_ROOT}/include
export LIB_DIR=${ORACLE_ROOT}/lib
make %{makeprocesses}

%install
mkdir %{i}/lib %{i}/bin
cp is_cxx11_abi %{i}/bin/
cp lib%{n}.%{soext} %{i}/lib

