### RPM external bootstrap-driver 30.0
## NOCOMPILER
Source: cmsos
Requires: rpm

#danger! cms-common version is now hardwired below (and in bootstrap.file)

%prep
%build
%install
cp %{_sourcedir}/cmsos %{i}/
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


case %cmsplatf in
cc* )
  cc8_amd64_packagesWithProvides="libGL"
  cc8_amd64_platformSeeds="
    automake bash bzip2 bzip2-libs bzip2-devel coreutils-single e2fsprogs e2fsprogs-libs
    file file-libs fontconfig freetype gcc-c++ git glibc krb5-libs libaio
    libcom_err libgomp libICE libidn
    libSM libX11 libX11-devel libxcrypt libXcursor libXext
    libXext-devel libXft libXft-devel libXi libXinerama
    libXmu libXpm libXpm-devel libXrandr libXrender
    libglvnd-opengl mesa-libGL mesa-libGLU mesa-libGLU-devel
    java-1.8.0-openjdk-devel libtool m4 make
    ncurses ncurses-libs ncurses-devel nspr nss nss-devel nss-util
    openssl openssl-devel openssl-libs
    perl perl-interpreter perl-libs
    perl-Carp perl-CGI perl-constant perl-Data-Dumper perl-DBI
    perl-Digest-MD5 perl-Encode perl-Env perl-Exporter perl-ExtUtils-Embed
    perl-File-Path perl-File-Temp perl-Getopt-Long perl-IO perl-libnet
    perl-Memoize perl-PathTools perl-Scalar-List-Utils perl-Socket perl-Storable
    perl-Term-ANSIColor perl-Test-Harness perl-Text-ParseWords perl-Thread-Queue
    perl-Time-HiRes perl-Time-Local perl-YAML
    patch popt popt-devel python2 readline readline-devel rpm-build
    rsync tcl tcsh tk wget which zlib zsh"
  ;;
slc*)
  # Backward compatible seeds, so that old bootstrap does not suddenly stop working.
  platformSeeds="glibc glibc-32bit coreutils bash tcsh zsh pdksh perl
        tcl tk perl-Tk readline openssl ncurses XFree86-libs
        e2fsprogs krb5-libs freetype fontconfig XFree86-Mesa-libGLU
        XFree86-Mesa-libGL xorg-x11-deprecated-libs
        xorg-x11-libs xorg-x11-Mesa-libGLU xorg-x11-Mesa-libGL
        compat-libstdc++-33 fglrx_6_8_0 libidn"

  slc6_amd64_platformSeeds="glibc coreutils bash tcsh zsh perl tcl tk readline openssl ncurses e2fsprogs krb5-libs freetype compat-readline5 ncurses-libs perl-libs perl-ExtUtils-Embed
        fontconfig compat-libstdc++-33 libidn libX11 libXmu libSM libICE libXcursor
        libXext libXrandr libXft mesa-libGLU mesa-libGL e2fsprogs-libs libXi libXinerama libXft-devel
        libXrender libXpm libcom_err perl-Test-Harness libX11-devel libXpm-devel libXext-devel mesa-libGLU-devel
        nspr nss nss-util file file-libs readline zlib popt bzip2 bzip2-libs"

  slc7_amd64_platformSeeds="glibc coreutils bash tcsh zsh perl tcl tk readline openssl ncurses e2fsprogs krb5-libs freetype ncurses-libs perl-libs perl-ExtUtils-Embed
        fontconfig compat-libstdc++-33 libidn libX11 libXmu libSM libICE libXcursor
        libXext libXrandr libXft mesa-libGLU mesa-libGL e2fsprogs-libs libXi libXinerama libXft-devel
        libXrender libXpm libcom_err perl-Test-Harness perl-Carp perl-constant perl-PathTools
        perl-Data-Dumper perl-Digest-MD5 perl-Exporter perl-File-Path perl-File-Temp perl-Getopt-Long
        perl-Socket perl-Text-ParseWords perl-Time-Local libX11-devel libXpm-devel libXext-devel mesa-libGLU-devel
        perl-Switch perl-Storable perl-Env perl-Thread-Queue perl-Encode nspr nss nss-util file file-libs readline
        zlib popt bzip2 bzip2-libs"

  slc7_aarch64_platformSeeds="glibc coreutils bash tcsh zsh perl tcl tk readline openssl
                              ncurses e2fsprogs krb5-libs freetype fontconfig libstdc++
                              libidn libX11 libXmu libSM libICE libXcursor libXext libXrandr
                              libXft mesa-libGLU mesa-libGL e2fsprogs-libs libXi libXinerama
                              libXrender libXpm gcc-c++ libcom_err libXpm-devel libXft-devel
                              libX11-devel libXext-devel mesa-libGLU mesa-libGLU-devel libGLEW
                              glew perl-Digest-MD5 perl-ExtUtils-MakeMaker patch perl-libwww-perl
                              krb5-libs krb5-devel perl-Data-Dumper perl-WWW-Curl texinfo hostname
                              time perl-Carp perl-Text-ParseWords perl-PathTools perl-ExtUtils-MakeMaker
                              perl-Exporter perl-File-Path perl-Getopt-Long perl-constant perl-File-Temp
                              perl-Socket perl-Time-Local perl-Storable glibc-headers perl-threads
                              perl-Thread-Queue perl-Module-ScanDeps perl-Test-Harness perl-Env perl-Switch
                              perl-ExtUtils-Embed ncurses-libs perl-libs nspr nss nss-util file file-libs
                              readline zlib popt bzip2 bzip2-libs perl-Encode"

  slc7_ppc64le_platformSeeds="glibc coreutils bash tcsh zsh perl tcl tk readline openssl
                              ncurses e2fsprogs krb5-libs freetype fontconfig libstdc++
                              libidn libX11 libXmu libSM libICE libXcursor libXext libXrandr
                              libXft mesa-libGLU mesa-libGL e2fsprogs-libs libXi libXinerama
                              libXrender libXpm gcc-c++ libcom_err libXpm-devel libXft-devel
                              libX11-devel libXext-devel mesa-libGLU mesa-libGLU-devel libGLEW
                              glew perl-Digest-MD5 perl-ExtUtils-MakeMaker patch perl-libwww-perl
                              krb5-libs krb5-devel perl-Data-Dumper perl-WWW-Curl texinfo hostname
                              time perl-Carp perl-Text-ParseWords perl-PathTools perl-ExtUtils-MakeMaker
                              perl-Exporter perl-File-Path perl-Getopt-Long perl-constant perl-File-Temp
                              perl-Socket perl-Time-Local perl-Storable glibc-headers perl-threads
                              perl-Thread-Queue perl-Module-ScanDeps perl-Test-Harness perl-Env perl-Switch
                              perl-ExtUtils-Embed ncurses-libs perl-libs nspr nss nss-util file file-libs
                              readline zlib popt bzip2 bzip2-libs perl-Encode"

  ;;
fc*)
  fc18_armv7hl_platformSeeds="glibc coreutils bash tcsh zsh perl tcl tk readline openssl 
                              ncurses e2fsprogs krb5-libs freetype fontconfig libstdc++
                              libidn libX11 libXmu libSM libICE libXcursor libXext libXrandr 
                              libXft mesa-libGLU mesa-libGL e2fsprogs-libs libXi libXinerama 
                              libXft libXrender libXpm gcc-c++ libcom_err libXpm-devel libXft-devel
                              libX11-devel libXext-devel mesa-libGLU mesa-libGLU-devel libGLEW
                              glew perl-Digest-MD5 perl-ExtUtils-MakeMaker patch perl-libwww-perl
                              krb5-libs krb5-devel perl-Data-Dumper perl-WWW-Curl"

  fc19_armv7hl_platformSeeds="glibc coreutils bash tcsh zsh perl tcl tk readline openssl 
                              ncurses e2fsprogs krb5-libs freetype fontconfig libstdc++
                              libidn libX11 libXmu libSM libICE libXcursor libXext libXrandr 
                              libXft mesa-libGLU mesa-libGL e2fsprogs-libs libXi libXinerama 
                              libXrender libXpm gcc-c++ libcom_err libXpm-devel libXft-devel
                              libX11-devel libXext-devel mesa-libGLU mesa-libGLU-devel libGLEW
                              glew perl-Digest-MD5 perl-ExtUtils-MakeMaker patch perl-libwww-perl
                              krb5-libs krb5-devel perl-Data-Dumper"

  fc19_aarch64_platformSeeds="glibc coreutils bash tcsh zsh perl tcl tk readline openssl
                              ncurses e2fsprogs krb5-libs freetype fontconfig libstdc++
                              libidn libX11 libXmu libSM libICE libXcursor libXext libXrandr
                              libXft mesa-libGLU mesa-libGL e2fsprogs-libs libXi libXinerama
                              libXrender libXpm gcc-c++ libcom_err libXpm-devel libXft-devel
                              libX11-devel libXext-devel mesa-libGLU mesa-libGLU-devel libGLEW
                              glew perl-Digest-MD5 perl-ExtUtils-MakeMaker patch perl-libwww-perl
                              krb5-libs krb5-devel perl-Data-Dumper perl-WWW-Curl texinfo hostname
                              time perl-Carp perl-Text-ParseWords perl-PathTools perl-ExtUtils-MakeMaker
                              perl-Exporter perl-File-Path perl-Getopt-Long perl-constant perl-File-Temp
                              perl-Socket perl-Time-Local perl-Storable"

  fc22_ppc64le_platformSeeds="glibc coreutils bash tcsh zsh perl tcl tk readline openssl
                              ncurses e2fsprogs krb5-libs freetype fontconfig libstdc++
                              libidn libX11 libXmu libSM libICE libXcursor libXext libXrandr
                              libXft mesa-libGLU mesa-libGL e2fsprogs-libs libXi libXinerama
                              libXrender libXpm gcc-c++ libcom_err libXpm-devel libXft-devel
                              libX11-devel libXext-devel mesa-libGLU mesa-libGLU-devel libGLEW
                              glew perl-Digest-MD5 perl-ExtUtils-MakeMaker patch perl-libwww-perl
                              krb5-libs krb5-devel perl-Data-Dumper perl-WWW-Curl texinfo hostname
                              time perl-Carp perl-Text-ParseWords perl-PathTools perl-ExtUtils-MakeMaker
                              perl-Exporter perl-File-Path perl-Getopt-Long perl-constant perl-File-Temp
                              perl-Socket perl-Time-Local perl-Storable glibc-headers perl-threads
                              perl-Thread-Queue perl-Module-ScanDeps perl-Test-Harness perl-Env perl-Switch
                              perl-Term-ANSIColor perl-ExtUtils-Embed ncurses-libs perl-libs"

  fc22_ppc64_platformSeeds="glibc coreutils bash tcsh zsh perl tcl tk readline openssl
                            ncurses e2fsprogs krb5-libs freetype fontconfig libstdc++
                            libidn libX11 libXmu libSM libICE libXcursor libXext libXrandr
                            libXft mesa-libGLU mesa-libGL e2fsprogs-libs libXi libXinerama
                            libXrender libXpm gcc-c++ libcom_err libXpm-devel libXft-devel
                            libX11-devel libXext-devel mesa-libGLU mesa-libGLU-devel libGLEW
                            glew perl-Digest-MD5 perl-ExtUtils-MakeMaker patch perl-libwww-perl
                            krb5-libs krb5-devel perl-Data-Dumper perl-WWW-Curl texinfo hostname
                            time perl-Carp perl-Text-ParseWords perl-PathTools perl-ExtUtils-MakeMaker
                            perl-Exporter perl-File-Path perl-Getopt-Long perl-constant perl-File-Temp
                            perl-Socket perl-Time-Local perl-Storable glibc-headers perl-threads
                            perl-Thread-Queue perl-Module-ScanDeps perl-Test-Harness perl-Env perl-Switch
                            perl-Term-ANSIColor perl-ExtUtils-Embed ncurses-libs perl-libs"

  fc24_amd64_platformSeeds="glibc coreutils bash tcsh zsh perl tcl tk readline openssl
                            ncurses e2fsprogs krb5-libs freetype fontconfig libstdc++
                            libidn libX11 libXmu libSM libICE libXcursor libXext libXrandr
                            libXft mesa-libGLU mesa-libGL e2fsprogs-libs libXi libXinerama
                            libXrender libXpm gcc-c++ libcom_err libXpm-devel libXft-devel
                            libX11-devel libXext-devel mesa-libGLU mesa-libGLU-devel libGLEW
                            glew perl-Digest-MD5 perl-ExtUtils-MakeMaker patch perl-libwww-perl
                            krb5-libs krb5-devel perl-Data-Dumper perl-WWW-Curl texinfo hostname
                            time perl-Carp perl-Text-ParseWords perl-PathTools perl-ExtUtils-MakeMaker
                            perl-Exporter perl-File-Path perl-Getopt-Long perl-constant perl-File-Temp
                            perl-Socket perl-Time-Local perl-Storable glibc-headers perl-threads
                            perl-Thread-Queue perl-Module-ScanDeps perl-Test-Harness perl-Env perl-Switch
                            perl-Term-ANSIColor perl-ExtUtils-Embed ncurses-libs perl-libs perl-Errno
                            perl-IO perl-Memoize nspr nss nss-util file file-libs readline zlib popt
                            bzip2 bzip2-libs perl-LWP-Protocol-connect perl-Encode"

  fc24_ppc64le_platformSeeds="glibc coreutils bash tcsh zsh perl tcl tk readline openssl
                              ncurses e2fsprogs krb5-libs freetype fontconfig libstdc++
                              libidn libX11 libXmu libSM libICE libXcursor libXext libXrandr
                              libXft mesa-libGLU mesa-libGL e2fsprogs-libs libXi libXinerama
                              libXrender libXpm gcc-c++ libcom_err libXpm-devel libXft-devel
                              libX11-devel libXext-devel mesa-libGLU mesa-libGLU-devel libGLEW
                              glew perl-Digest-MD5 perl-ExtUtils-MakeMaker patch perl-libwww-perl
                              krb5-libs krb5-devel perl-Data-Dumper perl-WWW-Curl texinfo hostname
                              time perl-Carp perl-Text-ParseWords perl-PathTools perl-ExtUtils-MakeMaker
                              perl-Exporter perl-File-Path perl-Getopt-Long perl-constant perl-File-Temp
                              perl-Socket perl-Time-Local perl-Storable glibc-headers perl-threads
                              perl-Thread-Queue perl-Module-ScanDeps perl-Test-Harness perl-Env perl-Switch
                              perl-Term-ANSIColor perl-ExtUtils-Embed ncurses-libs perl-libs perl-Errno
                              perl-IO perl-Memoize nspr nss nss-util file file-libs readline zlib popt
                              bzip2 bzip2-libs perl-LWP-Protocol-connect perl-Encode"

  fc24_ppc64_platformSeeds="glibc coreutils bash tcsh zsh perl tcl tk readline openssl
                            ncurses e2fsprogs krb5-libs freetype fontconfig libstdc++
                            libidn libX11 libXmu libSM libICE libXcursor libXext libXrandr
                            libXft mesa-libGLU mesa-libGL e2fsprogs-libs libXi libXinerama
                            libXrender libXpm gcc-c++ libcom_err libXpm-devel libXft-devel
                            libX11-devel libXext-devel mesa-libGLU mesa-libGLU-devel libGLEW
                            glew perl-Digest-MD5 perl-ExtUtils-MakeMaker patch perl-libwww-perl
                            krb5-libs krb5-devel perl-Data-Dumper perl-WWW-Curl texinfo hostname
                            time perl-Carp perl-Text-ParseWords perl-PathTools perl-ExtUtils-MakeMaker
                            perl-Exporter perl-File-Path perl-Getopt-Long perl-constant perl-File-Temp
                            perl-Socket perl-Time-Local perl-Storable glibc-headers perl-threads
                            perl-Thread-Queue perl-Module-ScanDeps perl-Test-Harness perl-Env perl-Switch
                            perl-Term-ANSIColor perl-ExtUtils-Embed ncurses-libs perl-libs perl-Errno
                            perl-IO perl-Memoize nspr nss nss-util file file-libs readline zlib popt
                            bzip2 bzip2-libs perl-LWP-Protocol-connect perl-Encode"
  ;;
esac

# Seeds for unsupported platforms. These will not make bootstrap die, if not found.
# OpenSuse
unsupportedSeeds="xorg-x11-Mesa compat-readline4 compat-curl2 freetype2
        xorg-x11-libX11"
# Ubuntu
unsupportedSeeds="$unsupportedSeeds libcomerr2 libidn11 libxi6 libxpm4 libxinerama1
        libncurses5 libsm6 libice6 libc6 libxcursor1 libxmu6
        libgl1-mesa-glx libxft2 perl-base xserver-xorg xserver-xorg-core
        libfreetype6 libfontconfig1 libgl1-mesa libxrandr2 libglu1-mesa
        libxext6 libx11-6 libxrender1"
# Fedora
unsupportedSeeds="$unsupportedSeeds libX11 libXmu libSM libICE libXcursor
        libXext libXrandr libXft mesa-libGLU mesa-libGL e2fsprogs-libs libXi libXinerama
        libXft libXrender libXpm ncurses-libs libc6-i686 compat-readline5"

# PU-IAS
unsupportedSeeds="$unsupportedSeeds libcom_err"

# Case statement for additional provides.
case %cmsplatf in
    osx* )
        additionalProvides="AGL ApplicationServices Carbon CoreFoundation
                            CoreServices OpenGL Python QuickTime Tcl Tk
                            libintl.3.dylib libperl.dylib"

    ;;
    # Required to get slc5_amd64_gcc434 work on slc6.
    slc*|cc* )
        additionalProvides="perl(CGI)"
    ;;
esac

unsupportedProvides="libtcl8.3.so libtk8.3.so /bin/env libcom_err.so.3
        libcrypto.so.4 libgssapi_krb5.so.2 libk5crypto.so.3
        libkrb5.so.3 libssl.so.4 /bin/csh /bin/tcsh libreadline.so.4
        libtcl8.4.so libtk8.4.so"

defaultPkgs="cms+cms-common+1.0"

mkdir -p %{i}/etc/profile.d
(echo "rpm_version=$RPM_VERSION"; \
 echo "platformSeeds=\"$platformSeeds\""; \
 echo "%{cmsos}_platformSeeds=\"$%{cmsos}_platformSeeds\""; \
 echo "%{cmsos}_packagesWithProvides=\"$%{cmsos}_packagesWithProvides\""; \
 echo "packageList=\"`echo $packageList`\""; \
 echo "additionalProvides=\"$additionalProvides\""; \
 echo "defaultPkgs=\"$defaultPkgs\""; \
) > %{i}/%{cmsplatf}-driver.txt

(echo "rpm_version=$RPM_VERSION"; \
 echo "platformSeeds=\"$platformSeeds $compPackages\""; \
 echo "%{cmsos}_platformSeeds=\"$%{cmsos}_platformSeeds\""; \
 echo "%{cmsos}_packagesWithProvides=\"$%{cmsos}_packagesWithProvides\""; \
 echo "packageList=\"`echo $packageList`\""; \
 echo "additionalProvides=\"$additionalProvides\""; \
 echo "defaultPkgs=\"$defaultPkgs\""; \
) > %{i}/%{cmsplatf}-driver-comp.txt

