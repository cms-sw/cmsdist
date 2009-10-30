### RPM cms coral CORAL_2_3_2
## IMPORT configurations 
Provides: /bin/zsh
Provides: libexpat.so.0
Requires: coral-tool-conf
Patch: coral-2_3_2-includes 
%define closingbrace )
%define online %(case %cmsplatf in *onl_*_*%closingbrace echo true;; *%closingbrace echo false;; esac)

%define cvsprojuc       %(echo %n | sed -e "s|-debug||"| tr 'a-z' 'A-Z')
%define cvsprojlc       %(echo %cvsprojuc | tr 'A-Z' 'a-z')
%define cvsdir          %cvsprojlc
%define cvsserver       %cvsprojlc
%define preBuildCommand (rm -rf LFCLookupService LFCReplicaService MySQLAccess)
%define prebuildtarget  prebuild
%define buildtarget     release-build

%define patchsrc    %patch -p0

%if "%online" == "true"
# Disable building tests in online release,
# since they bring dependency on cppunit:
%define patchsrc4       perl -p -i -e 's!(<classpath.*/tests\\+.*>)!!;' config/BuildFile.xml
%define patchsrc5       rm -rf src/UnitTests
%endif

%if "%(echo %{cmsos} | cut -d_ -f 1 | sed -e 's|osx.*|osx|')" == "osx"
%define patchsrc4    echo "<use name=boost>" >>src/UnitTests/BuildFile
# Disable building tests, since they bring dependency on cppunit:
%define patchsrc5       perl -p -i -e 's!(<classpath.*/tests\\+.*>)!!;' config/BuildFile.xml
%endif

## IMPORT lcg-scram-build
## IMPORT cms-scram-build
## IMPORT scramv1-build
