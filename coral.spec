### RPM cms coral CORAL_2_3_10
Provides: /bin/zsh
Provides: libexpat.so.0
Requires: coral-tool-conf
Patch: coral-2_3_10_MsgReporter_lrt
%define closingbrace )
%define online %(case %cmsplatf in *onl_*_*%closingbrace echo true;; *%closingbrace echo false;; esac)

%define cvssrc          %n
%define cvsrepo         cvs://:pserver:anonymous@%n.cvs.cern.ch/cvs/%n?passwd=Ah<Z

%define preBuildCommand (rm -rf LFCLookupService LFCReplicaService MySQLAccess)

%define patchsrc    %patch -p0

%if "%online" == "true"
# Disable building tests, since they bring dependency on cppunit:
%define patchsrc4       perl -p -i -e 's!(<classpath.*/tests\\+.*>)!!;' config/BuildFile.xml
%define patchsrc5       rm -rf src/UnitTests
%else
%if "%(echo %{cmsos} | cut -d_ -f 1 | sed -e 's|osx.*|osx|')" == "osx"
# Disable building tests, since they bring dependency on cppunit:
%define patchsrc4       perl -p -i -e 's!(<classpath.*/tests\\+.*>)!!;' config/BuildFile.xml
%define patchsrc5       echo "<use name=boost>" >>src/UnitTests/BuildFile
%endif
%endif

## IMPORT scram-project-build
