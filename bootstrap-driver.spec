### RPM external bootstrap-driver 32.0
## NOCOMPILER
Requires: rpm
BuildRequires: cms-common

#danger! cms-common version is now hardwired below (and in bootstrap.file)

%prep
%build
%install
packageList=""
echo requiredtools `echo %{requiredtools} | sed -e's|\s+| |;s|^\s+||'`
for tool in `echo %{requiredtools} | sed -e's|\s+| |;s|^\s+||'`
do
    case X$tool in
        Xdistcc|Xccache )
        ;;
        * )
            toolcap=`echo $tool | tr a-z- A-Z_`
            toolversion=$(eval echo $`echo ${toolcap}_VERSION`)
            toolrevision=$(eval echo $`echo ${toolcap}_REVISION`)
            echo $toolversion $toolrevision
            packageList="$packageList external+${tool}+${toolversion}-1-${toolrevision}.%cmsplatf.rpm"
        ;;
    esac
done

additionalProvides=""
defaultSeeds="glibc glibc-32bit coreutils bash tcsh zsh pdksh perl tcl tk perl-Tk readline openssl ncurses XFree86-libs
        e2fsprogs krb5-libs freetype fontconfig XFree86-Mesa-libGLU XFree86-Mesa-libGL xorg-x11-deprecated-libs
        xorg-x11-libs xorg-x11-Mesa-libGLU xorg-x11-Mesa-libGL compat-libstdc++-33 fglrx_6_8_0 libidn"
##############################
# Packages to seed for runtime
##############################
platformSeeds="bash bzip2-libs glibc nspr nss nss-util perl popt zlib glibc-devel openssl openssl-devel openssl-libs krb5-libs
      libcom_err tcsh perl-Carp perl-Data-Dumper perl-Exporter perl-File-Path perl-File-Temp perl-Getopt-Long perl-PathTools perl-Text-ParseWords
      perl-Thread-Queue perl-constant perl-Digest-MD5 perl-Socket libX11 libXext libXft libXpm libglvnd-glx libglvnd-opengl mesa-libGLU"
# Needed by python runtime
platformSeeds+=" readline ncurses-libs tcl tk"
# Seed packages which provides these
packagesWithProvides="/usr/bin/python3 /usr/bin/perl /usr/bin/env /usr/bin/uname"

##############################
#Packages to seed for build
##############################
platformBuildSeeds="git patch make zip unzip bzip2 java-1.8.0-openjdk-devel libcom_err-devel which libXpm-devel libXft-devel mesa-libGLU-devel rsync"
#needed by python build
platformBuildSeeds+=" readline-devel ncurses-devel tcl-devel tk-devel"
packagesWithBuildProvides=""

case %cmsplatf in
*_aarch64_* )
  ;;
*)
  # Needed by oracle
  platformSeeds+=" libaio"
  ;;
esac

case %cmsplatf in
cc* )
  platformSeeds+=" libxcrypt perl-IO"
  ;;
slc*)
  platformSeeds+=" perl-Switch"
  ;;
esac

# Seeds for unsupported platforms. These will not make bootstrap die, if not found.
# OpenSuse
unsupportedSeeds="xorg-x11-Mesa compat-readline4 compat-curl2 freetype2 xorg-x11-libX11"
# Ubuntu
unsupportedSeeds="$unsupportedSeeds libcomerr2 libidn11 libxi6 libxpm4 libxinerama1 libncurses5 libsm6 libice6 libc6 libxcursor1 libxmu6
        libgl1-mesa-glx libxft2 perl-base xserver-xorg xserver-xorg-core libfreetype6 libfontconfig1 libgl1-mesa libxrandr2 libglu1-mesa libxext6 libx11-6 libxrender1"
# Fedora
unsupportedSeeds="$unsupportedSeeds libX11 libXmu libSM libICE libXcursor
        libXext libXrandr libXft mesa-libGLU mesa-libGL e2fsprogs-libs libXi libXinerama
        libXft libXrender libXpm ncurses-libs libc6-i686 compat-readline5"
# PU-IAS
unsupportedSeeds="$unsupportedSeeds libcom_err"

defaultPkgs="cms+cms-common+1.0"

mkdir -p %{i}/etc/profile.d
(echo "rpm_version=$RPM_VERSION"; \
 echo "platformSeeds=\"$defaultSeeds\""; \
 echo "unsupportedSeeds=\"$unsupportedSeeds\""; \
 echo "%{cmsos}_platformSeeds=\"$platformSeeds\""; \
 echo "%{cmsos}_platformBuildSeeds=\"$platformBuildSeeds\""; \
 echo "%{cmsos}_packagesWithProvides=\"$packagesWithProvides\""; \
 echo "%{cmsos}_packagesWithBuildProvides=\"$packagesWithBuildProvides\""; \
 echo "packageList=\"$packageList\""; \
 echo "additionalProvides=\"$additionalProvides\""; \
 echo "defaultPkgs=\"$defaultPkgs\""; \
) > %{i}/%{cmsplatf}-driver.txt

cp %{i}/%{cmsplatf}-driver.txt %{i}/%{cmsplatf}-driver-comp.txt
