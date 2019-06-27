### RPM external oracle-fake 11.2.0.3.0__10.2.0.4.0
## INITENV SET ORACLE_HOME %{i}
## INITENV +PATH SQLPATH %{i}/bin

%define tag 6da7ab5b4643b54f57002f9c96c426355a960eb1
Source: https://github.com/cms-externals/oracle-fake/archive/%{tag}.tar.gz

%prep
%setup -n oracle-fake-%{tag}

%build
# NOP

%install
mkdir -p %{i}/{bin,lib}

cp -r include %{i}

g++ -shared -fPIC -o libocci.so occi.cc
g++ -shared -fPIC -o libclntsh.so clntsh.cc

cp *.so %{i}/lib
# bla bla
