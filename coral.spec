### RPM cms coral CORAL_2_3_21
Requires: coral-tool-conf
Patch0: coral-2_3_20-macosx
Patch1: coral-2_3_21-slc6
Patch3: coral-CORAL_2_3_20-hide-strict-aliasing
Patch4: coral-CORAL_2_3_20-remove-lost-dependencies
Patch5: coral-CORAL_2_3_21-move-to-libuuid

%define online %(case %cmsplatf in (*onl_*_*) echo true;; (*) echo false;; esac)

%define cvssrc          %n
%define cvsrepo         cvs://:pserver:anonymous@%n.cvs.cern.ch/cvs/%n?passwd=Ah<Z&force=1

%if "%online" == "true"
# Disable building tests, since they bring dependency on cppunit:
%define patchsrc4       perl -p -i -e 's!(<classpath.*/tests\\+.*>)!!;' config/BuildFile.xml
# Build with debug symbols, and package them in a separate rpm:
#subpackage debug disabledes
%endif

%if "%(echo %{cmsos} | cut -d_ -f 1 | sed -e 's|osx.*|osx|')" == "osx"
# Disable building tests, since they bring dependency on cppunit:
%define patchsrc4       perl -p -i -e 's!(<classpath.*/tests\\+.*>)!!;' config/BuildFile.xml
%define patchsrc3       %patch0 -p1 
%endif

%define patchsrc5       %patch5 -p0
%define patchsrc6       %patch1 -p0
%define patchsrc8       %patch3 -p0
%define patchsrc9       %patch4 -p0

## IMPORT scram-project-build
# For now disable SUBPACKAGE as it is causing problem calculating checksum
# Looks like sub package support in V00-22/21 is not working
# SUBPACKAGE debug IF %subpackageDebug
