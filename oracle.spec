### RPM external oracle 10.2.0.3
## INITENV SET ORACLE_HOME %i

# TODO:  actually there is an instantclient for OSX now...  we could make it deployable
Provides: libgcc_s.so.1()(64bit)
Provides: libgcc_s.so.1(GCC_3.0)(64bit)
%if "%(echo %cmsplatf | cut -b 1,2,3 )" == "osx"
Source0: none
%else
Source0: http://cmsrep.cern.ch/cmssw/oracle-mirror/%cmsos/%realversion/basic-%cmsos.zip
Source1: http://cmsrep.cern.ch/cmssw/oracle-mirror/%cmsos/%realversion/sdk-%cmsos.zip
Source2: http://cmsrep.cern.ch/cmssw/oracle-mirror/%cmsos/%realversion/sqlplus-%cmsos.zip
Source3: none
Source4: none
Source5: none
Source9: oracle-license
Source10: http://www.oracle.com/technology/tech/oci/occi/downloads/occi_gcc343_102020.tar.gz
%if "%{cmsos}" == "slc4_ia32"
Source3: http://cmsrep.cern.ch/cmssw/oracle-mirror/slc4_amd64/%realversion/basic-slc4_amd64.zip
Source4: http://cmsrep.cern.ch/cmssw/oracle-mirror/slc4_amd64/%realversion/sdk-slc4_amd64.zip
Source5: http://cmsrep.cern.ch/cmssw/oracle-mirror/slc4_amd64/%realversion/sqlplus-slc4_amd64.zip
%endif
%endif

## INITENV +PATH SQLPATH %i/bin
%prep
case %cmsos in
    osx* )
    ;;
    slc4_ia32 )
      rm -rf instantclient_*
      rm -rf libocci.so.10.1 libocci10.a 
      unzip -o -u %_sourcedir/basic-%cmsos.zip
      unzip -o -u %_sourcedir/sdk-%cmsos.zip
      unzip -o -u %_sourcedir/sqlplus-%cmsos.zip
      rm -rf oracle64; mkdir oracle64
      cd oracle64
      unzip -o -u %_sourcedir/basic-slc4_amd64.zip
      unzip -o -u %_sourcedir/sdk-slc4_amd64.zip
      unzip -o -u %_sourcedir/sqlplus-slc4_amd64.zip
      cd ..
      ;;
    * )
        rm -rf instantclient_*
        rm -rf libocci.so.10.1 libocci10.a 
        unzip -o -u %_sourcedir/basic-%cmsos.zip
        unzip -o -u %_sourcedir/sdk-%cmsos.zip
        unzip -o -u %_sourcedir/sqlplus-%cmsos.zip
    ;;
esac

%if "%{realversion}" == "10.2.0.3"
case %cmsos in 
    slc4_ia32 )
        tar xzvf %_sourcedir/occi_gcc343_102020.tar.gz
	cd oracle64
	tar xzvf %_sourcedir/occi_gcc343_102020.tar.gz
    ;;
esac
%endif

%build
%install
mkdir -p %i/bin %i/etc/profile.d %i/lib %i/admin %i/java %i/demo %i/include
cp %_sourcedir/oracle-license %{i}/oracle-license
cp -p instantclient*/lib* %i/lib
cp -p instantclient*/sqlplus %i/bin
cp -p instantclient*/glogin.sql %i/bin
cp -p instantclient*/*.jar %i/java
cp -p instantclient*/sdk/demo/* %i/demo
cp -p instantclient*/sdk/include/* %i/include
%if "%cmsplatf" == "slc4_ia32_gcc345"
echo Copying libocci libraries for slc4_ia32_gcc345
[ -f libocci.so.10.1 ] && mv libocci.so.10.1 %i/lib
[ -f libocci10.a ] && mv libocci10.a %i/lib
mkdir %i/oracle64
mkdir -p %i/oracle64/bin %i/oracle64/lib %i/oracle64/admin %i/oracle64/java %i/oracle64/demo %i/oracle64/include
cp -p oracle64/instantclient*/lib* %i/oracle64/lib
cp -p oracle64/instantclient*/sqlplus %i/oracle64/bin
cp -p oracle64/instantclient*/glogin.sql %i/oracle64/bin
cp -p oracle64/instantclient*/*.jar %i/oracle64/java
cp -p oracle64/instantclient*/sdk/demo/* %i/oracle64/demo
cp -p oracle64/instantclient*/sdk/include/* %i/oracle64/include
(cd %i/oracle64/lib && ln -s libclntsh.* $(echo libclntsh.* | sed 's/[0-9.]*$//'))
(cd %i/oracle64/lib && ln -s libocci.* $(echo libocci.* | sed 's/[0-9.]*$//'))
cat << \EOF_SLC4_64BIT_ENV_SCRIPT_SH >%i/etc/profile.d/init64.sh
#!/bin/sh
bostype=`uname`:`uname -p`
case $bostype in
  Linux:i*86 )
    if ldd /usr/bin/gcc | grep -q /lib64/ ; then
      bostype=Linux:x86_64
    fi
  ;;
esac
case $bostype in
  Linux:x86_64 )
    PATH="%i/oracle64/bin:$PATH"; export PATH
    LD_LIBRARY_PATH="%i/oracle64/lib:$LD_LIBRARY_PATH"; export LD_LIBRARY_PATH
    DYLD_FALLBACK_LIBRARY_PATH="%i/oracle64/lib:$DYLD_FALLBACK_LIBRARY_PATH"; export DYLD_FALLBACK_LIBRARY_PATH
    SQLPATH="%i/oracle64/bin:$SQLPATH"; export SQLPATH
  ;;
esac
EOF_SLC4_64BIT_ENV_SCRIPT_SH
cat << \EOF_SLC4_64BIT_ENV_SCRIPT_CSH >%i/etc/profile.d/init64.csh
#!/bin/csh
set bostype=`uname`:`uname -p`
switch ($bostype)
  case Linux:i*86:
    ldd /usr/bin/gcc | grep -q /lib64/
    if  ("X$?" == "X0") set bostype=Linux:x86_64
    breaksw
endsw
switch ($bostype)
  case Linux:x86_64:
    setenv PATH "%i/oracle64/bin:$PATH"
    setenv LD_LIBRARY_PATH "%i/oracle64/lib:$LD_LIBRARY_PATH"
    setenv DYLD_FALLBACK_LIBRARY_PATH "%i/oracle64/lib:$DYLD_FALLBACK_LIBRARY_PATH"
    setenv SQLPATH "%i/oracle64/bin:$SQLPATH"
    breaksw
endsw
EOF_SLC4_64BIT_ENV_SCRIPT_CSH
%endif
(cd %i/lib && ln -s libclntsh.* $(echo libclntsh.* | sed 's/[0-9.]*$//'))
(cd %i/lib && ln -s libocci.* $(echo libocci.* | sed 's/[0-9.]*$//'))
chmod -R g-w %i
touch %i/etc/profile.d/init64.sh
touch %i/etc/profile.d/init64.csh

# SCRAM ToolBox toolfile
mkdir -p %i/etc/scram.d
cat << \EOF_TOOLFILE >%i/etc/scram.d/%n
<doc type=BuildSystem::ToolDoc version=1.0>
<Tool name=%n version=%v>
<lib name=clntsh>
<lib name=occi>
<lib name=nnz10>
<Client>
 <Environment name=ORACLE_BASE default="%i"></Environment>
 <Environment name=ORACLE_ADMINDIR></Environment>
 <Environment name=LIBDIR value="$ORACLE_BASE/lib"></Environment>
 <Environment name=BINDIR value="$ORACLE_BASE/bin"></Environment>
 <Environment name=INCLUDE value="$ORACLE_BASE/include"></Environment>
</Client>
<use name=sockets>
<Runtime name=PATH value="$BINDIR" type=path>
<Runtime name=NLS_LANG value="american_america.WE8ISO8859P9">
<Runtime name=NLS_DATE_FORMAT value="DD-MON-FXYYYY">
<Runtime name=ORA_NLS33 default="$ORACLE_BASE/ocommon/nls/admin/data">
<Runtime name=ORACLE_HOME default="$ORACLE_BASE">
<Runtime name=TNS_ADMIN default="$ORACLE_ADMINDIR">
</Tool>
EOF_TOOLFILE
%post
echo ". $RPM_INSTALL_PREFIX/%{pkgrel}/etc/profile.d/init64.sh" >> $RPM_INSTALL_PREFIX/%{pkgrel}/etc/profile.d/init.sh
echo "source $RPM_INSTALL_PREFIX/%{pkgrel}/etc/profile.d/init64.csh" >> $RPM_INSTALL_PREFIX/%{pkgrel}/etc/profile.d/init.csh
%{relocateConfig}etc/scram.d/%n
%{relocateConfig}etc/profile.d/init64.sh
%{relocateConfig}etc/profile.d/init64.csh
