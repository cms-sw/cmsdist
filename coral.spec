### RPM cms coral CORAL_2_3_21
%define tag 4fc6c24175682aff2d4299765b47b603a7b218d2
%define branch cms/%{realversion}py3
%define github_user cms-externals

Patch0: coral-2_3_20-macosx
Patch1: coral-2_3_21-gcc8
Patch5: coral-2_3_21-py312
Requires: coral-tool-conf

%define cvssrc          %{n}

# Disable building tests, since they bring dependency on cppunit:
%ifarch darwin
%define patchsrc2        perl -p -i -e 's!(<classpath.*/tests\\+.*>)!!;' config/BuildFile.xml
%define patchsrc3       %patch0 -p1
%endif
%define patchsrc5       %patch5 -p1

# Drop Oracle interface on ARM machines and POWER machines.
# Oracle does not provide Instant Client for ARMv8 or POWER8.
%ifnarch x86_64
%define patchsrc2       rm -rf ./src/OracleAccess
%endif
%define patchsrc4       %patch1 -p1
%define patchsrc5       %patch5 -p1

%define source1  git://github.com/%{github_user}/%{n}.git?protocol=https&obj=%{branch}/%{tag}&module=%{cvssrc}&export=%{srctree}&output=/src.tar.gz
## SUBPACKAGE debug IF %subpackageDebug
## INCLUDE scram-project-build