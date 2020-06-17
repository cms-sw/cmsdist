### RPM external oracle 19.6.0.0.0dbru
## INITENV SET ORACLE_HOME %{i}
## INITENV +PATH SQLPATH %{i}/bin

AutoReq: no

%define http_mirror https://download.oracle.com/otn_software/linux/instantclient/19600
%define client_dir instantclient_19_6

# zip files contains overlapping files, use -o to avoid human input
%define __unzip unzip -o

%if %(case %{cmsplatf} in (*_ppc64le_*) echo 1 ;; (*) echo 0 ;; esac) == 1
%define client_arch linux.leppc64
%endif

%if %(case %{cmsplatf} in (*_ppc64_*) echo 1 ;; (*) echo 0 ;; esac) == 1
%define client_arch linux.ppc64.c64
%endif

%if %(case %{cmsplatf} in (osx*_amd64_*) echo 1 ;; (*) echo 0 ;; esac) == 1
%define client_arch macos.x64
%endif

%if %(case %{cmsplatf} in (*_amd64_*) echo 1 ;; (*) echo 0 ;; esac) == 1
%define client_arch linux.x64
%endif

Source0: %{http_mirror}/instantclient-basic-%{client_arch}-%{realversion}.zip
Source1: %{http_mirror}/instantclient-basiclite-%{client_arch}-%{realversion}.zip
Source2: %{http_mirror}/instantclient-jdbc-%{client_arch}-%{realversion}.zip
Source3: %{http_mirror}/instantclient-odbc-%{client_arch}-%{realversion}.zip
Source4: %{http_mirror}/instantclient-sdk-%{client_arch}-%{realversion}.zip
Source5: %{http_mirror}/instantclient-sqlplus-%{client_arch}-%{realversion}.zip
Source6: %{http_mirror}/instantclient-tools-%{client_arch}-%{realversion}.zip

Source10: oracle-license

%prep
rm -rf instantclient_*

%setup -D -T -b 0 -n %{client_dir} instantclient-basic-%{client_arch}-%{realversion}.zip
%setup -D -T -b 1 -n %{client_dir} instantclient-basiclite-%{client_arch}-%{realversion}.zip
%setup -D -T -b 2 -n %{client_dir} instantclient-jdbc-%{client_arch}-%{realversion}.zip
%setup -D -T -b 3 -n %{client_dir} instantclient-odbc-%{client_arch}-%{realversion}.zip
%setup -D -T -b 4 -n %{client_dir} instantclient-sdk-%{client_arch}-%{realversion}.zip
%setup -D -T -b 5 -n %{client_dir} instantclient-sqlplus-%{client_arch}-%{realversion}.zip
%setup -D -T -b 6 -n %{client_dir} instantclient-tools-linux-%{client_arch}-%{realversion}.zip

%build
chmod a-x sdk/include/*.h *.sql

%install
mkdir -p %{i}/{bin,lib,java,demo,include,doc,etc}
cp %{_sourcedir}/oracle-license   %{i}/etc/LICENSE
mv lib*                           %{i}/lib
mv glogin.sql                     %{i}/bin
mv *.jar sdk/*.zip                %{i}/java
mv sdk/demo/*                     %{i}/demo
mv sdk/include/*                  %{i}/include

for f in sqlplus adrci genezi uidrvci sdk/ott; do
  [ -f $f ] || continue
  mv $f %{i}/bin
done

cd %{i}/lib
for f in lib*.{dylib,so}.[0-9]*; do
  [ -f $f ] || continue
  dest=$(echo $f | sed 's/\.[.0-9]*$//')
  rm -f $dest
  ln -s $f $dest
done
