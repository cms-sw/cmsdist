### RPM cms coral CORAL_2_3_12
Requires: coral-tool-conf
Patch: coral-2_3_12-SearchPath
Patch2: coral-2_3_12-FrontierAccess
Patch3: coral-2_3_12-macosx
Patch4: coral-2_3_12-fix-new-boost

%define online %(case %cmsplatf in (*onl_*_*) echo true;; (*) echo false;; esac)

%define cvssrc          %n
%define cvsrepo         cvs://:pserver:anonymous@%n.cvs.cern.ch/cvs/%n?passwd=Ah<Z&force=1

%define patchsrc    %patch -p0
%define patchsrc2   %patch2 -p0

%if "%online" == "true"
# Disable building tests, since they bring dependency on cppunit:
%define patchsrc4       perl -p -i -e 's!(<classpath.*/tests\\+.*>)!!;' config/BuildFile.xml
# Build with debug symbols, and package them in a separate rpm:
#define subpackageDebug yes
%endif

%if "%(echo %{cmsos} | cut -d_ -f 1 | sed -e 's|osx.*|osx|')" == "osx"
# Disable building tests, since they bring dependency on cppunit:
%define patchsrc4       perl -p -i -e 's!(<classpath.*/tests\\+.*>)!!;' config/BuildFile.xml
%define patchsrc5       %patch3 -p1
%endif
%define patchsrc7       %patch4 -p0

## IMPORT scram-project-build
