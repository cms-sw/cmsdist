### RPM external oracle-fake 11.2.0.3.0__10.2.0.4.0
## INITENV SET ORACLE_HOME %{i}
## INITENV +PATH SQLPATH %{i}/bin

Source: http://davidlt.web.cern.ch/davidlt/vault/final_fake/oracle-fake.tar.bz2

%prep
%setup -n oracle-fake

%build
# NOP

%install
mkdir -p %{i}/{bin,lib}

cp -r include %{i}

g++ -shared -fPIC -o libocci.so occi.cc
g++ -shared -fPIC -o libclntsh.so clntsh.cc

cp *.so %{i}/lib
