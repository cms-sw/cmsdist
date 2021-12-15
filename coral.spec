### RPM cms coral CORAL_2_3_21
%define tag 2ac0d2a14fe877702f5491fe66702a5d32039262
%define branch cms/%{realversion}py3
%define github_user cms-externals

Patch0: coral-2_3_20-macosx
Patch1: coral-2_3_21-gcc8
Requires: coral-tool-conf

%define cvssrc          %{n}

# Build with debug symbols, and package them in a separate rpm:
%define subpackageDebug yes

# Disable building tests, since they bring dependency on cppunit:
%ifarch darwin
%define patchsrc2        perl -p -i -e 's!(<classpath.*/tests\\+.*>)!!;' config/BuildFile.xml
%define patchsrc3       %patch0 -p1 
%endif

# Drop Oracle interface on ARM machines and POWER machines.
# Oracle does not provide Instant Client for ARMv8 or POWER8.
%ifnarch x86_64
%define patchsrc2       rm -rf ./src/OracleAccess
%endif
%define patchsrc4       %patch1 -p1

%define source1  git://github.com/%{github_user}/%{n}.git?protocol=https&obj=%{branch}/%{tag}&module=%{cvssrc}&export=%{srctree}&output=/src.tar.gz
## IMPORT scram-project-build
## SUBPACKAGE debug IF %subpackageDebug
