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

%define source0 instantclient-basic-linux.%{client_arch}-%{realversion}.zip
%define source1 instantclient-basiclite-linux.%{client_arch}-%{realversion}.zip
%define source2 instantclient-jdbc-linux.%{client_arch}-%{realversion}.zip
%define source3 instantclient-odbc-linux.%{client_arch}-%{realversion}.zip
%define source4 instantclient-sdk-linux.%{client_arch}-%{realversion}.zip
%define source5 instantclient-sqlplus-linux.%{client_arch}-%{realversion}.zip
%define source6 instantclient-tools-linux.%{client_arch}-%{realversion}.zip
%define source7 libocci.so.%{occi_lib}.zip

Source0: %{http_mirror}/%{source0}
Source1: %{http_mirror}/%{source1}
Source2: %{http_mirror}/%{source2}
Source3: %{http_mirror}/%{source3}
Source4: %{http_mirror}/%{source4}
Source5: %{http_mirror}/%{source5}
Source6: %{http_mirror}/%{source6}
Source7: http://cmsrep.cern.ch/cmssw/download/oracle-mirror/x64/%{source7}
Source10: oracle-license

%prep
rm -rf instantclient_*
#RPM 4.18 does not allow to override build-in %%__unzip, so we explicitly use it instead of calling %%setup
%{__unzip} -o -x %{_sourcedir}/%{source0}
%{__unzip} -o -x %{_sourcedir}/%{source1}
%{__unzip} -o -x %{_sourcedir}/%{source2}
%{__unzip} -o -x %{_sourcedir}/%{source3}
%{__unzip} -o -x %{_sourcedir}/%{source4}
%{__unzip} -o -x %{_sourcedir}/%{source5}
%{__unzip} -o -x %{_sourcedir}/%{source6}

%ifarch x86_64
#OCCI lib with new C++ ABI (GCC 5 and above)
%{__unzip} -o -x %{_sourcedir}/%{source7} -d %{client_dir}
%endif

chmod -Rf a+rX,u+w,g-w,o-w %{client_dir}

%build
cd %{client_dir}
chmod a-x sdk/include/*.h *.sql
%ifarch x86_64
chmod +x libocci_gcc53.so.%{occi_lib}
ln -sf libocci_gcc53.so.%{occi_lib} libocci.so.%{occi_lib}
%endif

%install
cd %{client_dir}
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
