%ifarch ppc64le
%define oc_ver 19.3.0.0.0dbru
%define client_arch leppc64.c64
%define ver_num 193
%endif
%ifarch aarch64
%define oc_ver 19.10.0.0.0dbru
%define client_arch arm64
%define ver_num 191000
%endif
%ifarch x86_64
%define oc_ver 19.11.0.0.0dbru
%define client_arch x64
%define ver_num 1911000
%endif
%define occi_lib 19.1

### RPM external oracle %{oc_ver}
## INITENV SET ORACLE_HOME %{i}
## INITENV +PATH SQLPATH %{i}/bin

AutoReq: no

%define http_mirror https://download.oracle.com/otn_software/linux/instantclient/%{ver_num}
%define client_dir instantclient_%(echo %{oc_ver} | cut -d. -f1,2 | tr '.' '_')

# zip files contains overlapping files, use -o to avoid human input
%define __unzip unzip -o

%define source0 %{http_mirror}/instantclient-basic-linux.%{client_arch}-%{realversion}.zip
%define source1 %{http_mirror}/instantclient-basiclite-linux.%{client_arch}-%{realversion}.zip
%define source2 %{http_mirror}/instantclient-jdbc-linux.%{client_arch}-%{realversion}.zip
%define source3 %{http_mirror}/instantclient-odbc-linux.%{client_arch}-%{realversion}.zip
%define source4 %{http_mirror}/instantclient-sdk-linux.%{client_arch}-%{realversion}.zip
%define source5 %{http_mirror}/instantclient-sqlplus-linux.%{client_arch}-%{realversion}.zip
%define source6 %{http_mirror}/instantclient-tools-linux.%{client_arch}-%{realversion}.zip
%define source7 http://cmsrep.cern.ch/cmssw/download/oracle-mirror/x64/libocci.so.%{occi_lib}.zip

Source0: %{source0}
Source1: %{source1}
Source2: %{source2}
Source3: %{source3}
Source4: %{source4}
Source5: %{source5}
Source6: %{source6}
Source7: %{source7}
Source10: oracle-license

%prep
rm -rf instantclient_*

%setup -D -T -b 0 -n %{client_dir} %(echo %{source0} | sed 's|.*/||)
%setup -D -T -b 1 -n %{client_dir} %(echo %{source1} | sed 's|.*/||)
%setup -D -T -b 2 -n %{client_dir} %(echo %{source2} | sed 's|.*/||)
%setup -D -T -b 3 -n %{client_dir} %(echo %{source3} | sed 's|.*/||)
%setup -D -T -b 4 -n %{client_dir} %(echo %{source4} | sed 's|.*/||)
%setup -D -T -b 5 -n %{client_dir} %(echo %{source5} | sed 's|.*/||)
%setup -D -T -b 6 -n %{client_dir} %(echo %{source6} | sed 's|.*/||)

%ifarch x86_64
#OCCI lib with new C++ ABI (GCC 5 and above)
%setup -D -T -c -a 7 -n %{client_dir} %(echo %{source7} | sed 's|.*/||)
%endif

%build
chmod a-x sdk/include/*.h *.sql
%ifarch x86_64
chmod +x libocci_gcc53.so.%{occi_lib}
ln -sf libocci_gcc53.so.%{occi_lib} libocci.so.%{occi_lib}
%endif

%install
mkdir -p %{i}/{bin,lib,java,demo,include,doc,etc}
cp %{_sourcedir}/oracle-license   %{i}/etc/LICENSE
mv *_LICENSE                      %{i}/etc
mv *README*                       %{i}/doc
mv lib*                           %{i}/lib
mv glogin.sql                     %{i}/bin
mv *.jar sdk/*.zip                %{i}/java
mv sdk/demo/*                     %{i}/demo
mv sdk/include/*                  %{i}/include

for f in * sdk/*; do
  [ -f $f ] || continue
  [ -x $f ] || continue
  mv $f %{i}/bin
done

mv sdk network help               %{i}
cd %{i}/lib
for f in lib*.{dylib,so}.[0-9]*; do
  [ -f $f ] || continue
  dest=$(echo $f | sed 's/\.[.0-9]*$//')
  rm -f $dest
  ln -s $f $dest
done
