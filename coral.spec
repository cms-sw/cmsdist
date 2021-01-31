### RPM cms coral CORAL_2_3_21
Requires: coral-tool-conf
Patch0: coral-2_3_20-macosx
Patch2: coral-CORAL_2_3_20-boost150-fix
Patch3: coral-CORAL_2_3_20-hide-strict-aliasing
Patch4: coral-CORAL_2_3_20-remove-lost-dependencies
Patch5: coral-CORAL_2_3_21-move-to-libuuid
Patch6: coral-CORAL_2_3_21-forever-ttl

%define isonline %(case %{cmsplatf} in (*onl_*_*) echo 1 ;; (*) echo 0 ;; esac)
%define isarmv7 %(case %{cmsplatf} in (*armv7*) echo 1 ;; (*) echo 0 ;; esac)
%define isdarwin %(case %{cmsos} in (osx*) echo 1 ;; (*) echo 0 ;; esac)

%define cvssrc          %{n}
%define cvsrepo         cvs://:pserver:anonymous@%{n}.cvs.cern.ch/cvs/%{n}?passwd=Ah<Z&force=1

%if %isonline
# Disable building tests, since they bring dependency on cppunit:
%define patchsrc2       perl -p -i -e 's!(<classpath.*/tests\\+.*>)!!;' config/BuildFile.xml
# Build with debug symbols, and package them in a separate rpm:
#subpackage debug disabledes
%endif

# Disable building tests, since they bring dependency on cppunit:
%if %isdarwin
%define patchsrc3       perl -p -i -e 's!(<classpath.*/tests\\+.*>)!!;' config/BuildFile.xml
%define patchsrc        %patch0 -p1 
%endif

%define patchsrc4       %patch5 -p0
%define patchsrc5       %patch2 -p0
%define patchsrc6       %patch3 -p0
%define patchsrc7       %patch4 -p0
%define patchsrc9	%patch6 -p0

# Drop Oracle interface on ARM machines. 
# Oracle does not provide Instant Client for ARMv7/v8.
%if %isarmv7
%define patchsrc8       rm -rf ./src/OracleAccess
%endif

## IMPORT scram-project-build
# For now disable SUBPACKAGE as it is causing problem calculating checksum
# Looks like sub package support in V00-22/21 is not working
# SUBPACKAGE debug IF %subpackageDebug
