### RPM external bootstrap-driver 42.0
## NOCOMPILER
Requires: rpm
BuildRequires: cms-common fakesystem

#danger! cms-common version is now hardwired below (and in bootstrap.file)

%prep
%build
%install
packageList=""
for tool in $(echo %{directpkgreqs} | tr '/' '+') ; do
  packageList="$packageList ${tool}-1-1.%{cmsplatf}.rpm"
done

additionalProvides=""
##############################
# Packages to seed for runtime
##############################
platformSeeds="  bash glibc glibc-headers python3 openssl-libs"
platformSeeds+=" libbrotli libX11 libxcrypt"

# Needed by python runtime
platformSeeds+=" readline ncurses-libs tcl tk"

# Needed by root runtime
platformSeeds+=" mesa-libGLU libglvnd-glx libglvnd-opengl libXext libXft libXpm"

#Various packages perl dependencies
platformSeeds+=" perl perl-base perl-filetest perl-lib perl-libs perl-overload perl-vars"
  
#Various packages required by xrootd with krb5 enabled
platformSeeds+=" libcom_err krb5-libs"

# Seed packages which provides these
packagesWithProvides=" /usr/bin/python3 /usr/bin/env /usr/bin/uname /bin/sh /usr/bin/perl"

##############################
#Packages to seed for build
##############################
platformBuildSeeds="  git patch make zip unzip bzip2 which rsync"
platformBuildSeeds+=" openssl-devel brotli-devel libxcrypt-devel"
platformBuildSeeds+=" libX11-devel libXpm-devel libXft-devel mesa-libGLU-devel"
platformBuildSeeds+=" java-1.8.0-openjdk-devel"

#Various packages required by xrootd with krb5 enabled
platformBuildSeeds+=" libcom_err-devel krb5-devel"
  
#needed by python build
platformBuildSeeds+=" readline-devel ncurses-devel tcl-devel tk-devel"

##############################
#Packages which provides a definition
##############################
packagesWithBuildProvides=""

%ifnarch aarch64
# Needed by oracle
platformSeeds+=" libaio"
%endif

%if "%{rhel}" == "9"
platformSeeds+=" libgcc"
%endif

defaultPkgs="cms+cms-common+1.0 cms+fakesystem+1.0"

mkdir -p %{i}/etc/profile.d
(echo "rpm_version=$RPM_VERSION"; \
 echo "platformSeeds=\"\""; \
 echo "unsupportedSeeds=\"\""; \
 echo "%{cmsos}_platformSeeds=\"$platformSeeds\""; \
 echo "%{cmsos}_platformBuildSeeds=\"$platformBuildSeeds\""; \
 echo "%{cmsos}_packagesWithProvides=\"$packagesWithProvides\""; \
 echo "%{cmsos}_packagesWithBuildProvides=\"$packagesWithBuildProvides\""; \
 echo "packageList=\"$packageList\""; \
 echo "additionalProvides=\"$additionalProvides\""; \
 echo "defaultPkgs=\"$defaultPkgs\""; \
) > %{i}/%{cmsplatf}-driver.txt

cp %{i}/%{cmsplatf}-driver.txt %{i}/%{cmsplatf}-driver-comp.txt
