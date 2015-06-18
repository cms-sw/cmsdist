### RPM cms coral CORAL_2_3_21
Requires: coral-tool-conf
Patch0: coral-2_3_20-macosx
Patch2: coral-CORAL_2_3_20-boost150-fix
Patch3: coral-CORAL_2_3_20-hide-strict-aliasing
Patch4: coral-CORAL_2_3_20-remove-lost-dependencies
Patch5: coral-CORAL_2_3_21-move-to-libuuid
Patch6: coral-CORAL_2_3_21-forever-ttl
Patch7: coral-CORAL_2_3_21-fix-timestamp-sqlite
Patch8: coral-CORAL_2_3_21-fix-timestamp-frontier

%define isdarwin %(case %{cmsos} in (osx*) echo 1 ;; (*) echo 0 ;; esac)

%define cvssrc          %{n}

# Build with debug symbols, and package them in a separate rpm:
%define subpackageDebug yes

# Disable building tests, since they bring dependency on cppunit:
%if %isdarwin
%define patchsrc        perl -p -i -e 's!(<classpath.*/tests\\+.*>)!!;' config/BuildFile.xml
%define patchsrc2       %patch0 -p1 
%endif

%define patchsrc3       %patch5 -p0
%define patchsrc4       %patch2 -p0
%define patchsrc5       %patch3 -p0
%define patchsrc6       %patch4 -p0
%define patchsrc7       %patch6 -p0
%define patchsrc8       %patch7 -p1
%define patchsrc9       %patch8 -p1

%define source1 cvs://:pserver:anonymous@%{n}.cvs.cern.ch/cvs/%{n}?passwd=Ah<Z&force=1&tag=-r%{cvstag}&module=%{cvssrc}&export=%{srctree}&output=/src.tar.gz

## IMPORT scram-project-build
## SUBPACKAGE debug IF %subpackageDebug
