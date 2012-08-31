### RPM cms coral CORAL_2_3_21
Requires: coral-tool-conf
Patch0: coral-2_3_20-macosx

%define online %(case %cmsplatf in (*onl_*_*) echo true;; (*) echo false;; esac)

%define cvssrc          %n
%define cvsrepo         cvs://:pserver:anonymous@%n.cvs.cern.ch/cvs/%n?passwd=Ah<Z&force=1

%if "%online" == "true"
# Disable building tests, since they bring dependency on cppunit:
%define patchsrc4       perl -p -i -e 's!(<classpath.*/tests\\+.*>)!!;' config/BuildFile.xml
# Build with debug symbols, and package them in a separate rpm:
%define subpackageDebug yes
%endif

%if "%(echo %{cmsos} | cut -d_ -f 1 | sed -e 's|osx.*|osx|')" == "osx"
# Disable building tests, since they bring dependency on cppunit:
%define patchsrc4       perl -p -i -e 's!(<classpath.*/tests\\+.*>)!!;' config/BuildFile.xml
%define patchsrc5       %patch0 -p1
%endif

## IMPORT scram-project-build
## SUBPACKAGE debug IF %subpackageDebug
