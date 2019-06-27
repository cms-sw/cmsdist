### RPM external bootstrap-driver 23.0
## NOCOMPILER

Requires: rpm

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


case %cmsplatf in
slc*onl* )
    ##########################################################
    # Backward compatible seeds, so that old bootstrap does not suddenly stop working.
    platformSeeds="glibc coreutils bash tcsh zsh pdksh perl tcl
        readline ncurses
        e2fsprogs krb5-libs freetype fontconfig
        xorg-x11-deprecated-libs xorg-x11-libs xorg-x11-Mesa-libGLU
        xorg-x11-Mesa-libGL compat-libstdc++-33 libidn"

    # ONLINE: seed system compiler (only libraries for runtime)
    platformSeeds="$platformSeeds libgcc libstdc++"

    # ONLINE: seed other available system tools:
    platformSeeds="$platformSeeds libpng libtiff libungif qt zlib perl-DBI-1.40-8"

    # Python tools are commented out due to compatibility problems.
    platformSeeds="$platformSeeds python python-elementtree"

    # ONLINE: seed daq-built tools:
    platformSeeds="$platformSeeds daq-cgicc daq-mimetic daq-oracle daq-tinyproxy daq-xerces daq-xdaq"

    platformSeeds="$platformSeeds daq-config daq-log4cplus daq-logudpappender
        daq-logxmlappender daq-pt daq-ptfifo daq-pthttp
        daq-pttcp daq-toolbox daq-xcept daq-xdaq2rc daq-xdata
        daq-xgi daq-xoap daq-sentinelutils"

    ##########################################################
    #slc4onl_ia32 Specific
    slc4onl_ia32_platformSeeds="glibc coreutils bash tcsh zsh pdksh perl tcl
        readline openssl ncurses
        e2fsprogs krb5-libs freetype fontconfig
        xorg-x11-deprecated-libs xorg-x11-libs xorg-x11-Mesa-libGLU
        xorg-x11-Mesa-libGL compat-libstdc++-33 libidn"

    # ONLINE: seed system compiler (only libraries for runtime)
    slc4onl_ia32_platformSeeds="$slc4onl_ia32_platformSeeds libgcc libstdc++"

    # ONLINE: seed other available system tools:
    slc4onl_ia32_platformSeeds="$slc4onl_ia32_platformSeeds curl libpng libtiff libungif openssl qt zlib perl-DBI-1.40-8"

    # Python tools are commented out due to compatibility problems.
    slc4onl_ia32_platformSeeds="$slc4onl_ia32_platformSeeds python python-elementtree"

    # ONLINE: seed daq-built tools:
    slc4onl_ia32_platformSeeds="$slc4onl_ia32_platformSeeds daq-cgicc daq-mimetic daq-oracle daq-tinyproxy daq-xerces daq-xdaq"

    slc4onl_ia32_platformSeeds="$slc4onl_ia32_platformSeeds daq-config daq-log4cplus daq-logudpappender
        daq-logxmlappender daq-pt daq-ptfifo daq-pthttp
        daq-pttcp daq-toolbox daq-xcept daq-xdaq2rc daq-xdata
        daq-xgi daq-xoap daq-sentinelutils"

    ##########################################################
    #slc5onl_ia32 Specific
    slc5onl_ia32_platformSeeds="glibc coreutils bash tcsh zsh perl tcl tk readline ncurses e2fsprogs krb5-libs freetype
        fontconfig libidn libX11 libXmu libSM libICE libXcursor
        libXext libXrandr libXft mesa-libGLU mesa-libGL e2fsprogs-libs libXi libXinerama libXft
        libXrender libXpm"

    # ONLINE: seed system compiler (only libraries for runtime)
    slc5onl_ia32_platformSeeds="$slc5onl_ia32_platformSeeds libgcc libstdc++ external+gcc+4.3.4"

    # ONLINE: seed other available system tools:
    slc5onl_ia32_platformSeeds="$slc5onl_ia32_platformSeeds curl curl-devel openssl openssl-devel zlib zlib-devel e2fsprogs-libs e2fsprogs-devel
        perl-DBI-1.52 libtermcap-2.0.8 libX11-devel-1.0.3 libXpm-devel-3.5.5 libXext-devel-1.0.1 libXft-devel-2.1.10"

    # ONLINE: seed daq-built tools:
    slc5onl_ia32_platformSeeds="$slc5onl_ia32_platformSeeds daq-log4cplus daq-mimetic daq-oracle daq-sqlite daq-xdaq daq-xerces
        daq-appweb daq-asyncresolv daq-cgicc daq-tinyproxy daq-config daq-logudpappender
        daq-logxmlappender daq-pt daq-ptfifo daq-pthttp daq-pttcp daq-toolbox daq-xalan
        daq-xcept daq-xdaq2rc daq-xdata daq-xgi daq-xoap daq-sentinelutils"

    ##########################################################
    #slc5onl_amd64 Specific
    slc5onl_amd64_platformSeeds="glibc coreutils bash tcsh zsh perl tcl tk readline ncurses e2fsprogs krb5-libs freetype
        fontconfig libidn libX11 libXmu libSM libICE libXcursor
        libXext libXrandr libXft mesa-libGLU mesa-libGL e2fsprogs-libs libXi libXinerama libXft
        libXrender libXpm"

    # ONLINE: seed system compiler (only libraries for runtime) only for amd64_gcc434 arch
    case %cmsplatf in
        *_amd64_gcc434 ) slc5onl_amd64_platformSeeds="$slc5onl_amd64_platformSeeds libgcc libstdc++ external+gcc+4.3.4-onl64a" ;;
    esac

    # ONLINE: seed other available system tools:
    slc5onl_amd64_platformSeeds="$slc5onl_amd64_platformSeeds zlib zlib-devel e2fsprogs-libs e2fsprogs-devel
        perl-DBI-1.52 libtermcap-2.0.8 libX11-devel-1.0.3 libXpm-devel-3.5.5 libXext-devel-1.0.1 libXft-devel-2.1.10"

    # ONLINE: seed daq-built tools:
    slc5onl_amd64_platformSeeds="$slc5onl_amd64_platformSeeds daq-log4cplus daq-mimetic daq-oracle daq-sqlite daq-xdaq daq-xerces
        daq-appweb daq-asyncresolv daq-cgicc daq-tinyproxy daq-config daq-logudpappender
        daq-logxmlappender daq-pt daq-ptfifo daq-pthttp daq-pttcp daq-toolbox daq-xalan 
        daq-xcept daq-xdaq2rc daq-xdata daq-xgi daq-xoap daq-sentinelutils"

    ;;
slc*)
  # Backward compatible seeds, so that old bootstrap does not suddenly stop working.
  platformSeeds="glibc glibc-32bit coreutils bash tcsh zsh pdksh perl
        tcl tk perl-Tk readline openssl ncurses XFree86-libs
        e2fsprogs krb5-libs freetype fontconfig XFree86-Mesa-libGLU
        XFree86-Mesa-libGL xorg-x11-deprecated-libs
        xorg-x11-libs xorg-x11-Mesa-libGLU xorg-x11-Mesa-libGL
        compat-libstdc++-33 fglrx_6_8_0 libidn"
  # Platform specific seeds. These are mandatory and the new bootstrap.sh will refuse continuing in the case they are not found.
  slc4_ia32_platformSeeds="glibc coreutils bash tcsh zsh pdksh perl
        tcl tk perl-Tk readline openssl ncurses XFree86-libs
        e2fsprogs krb5-libs freetype fontconfig XFree86-Mesa-libGLU
        XFree86-Mesa-libGL xorg-x11-deprecated-libs
        xorg-x11-libs xorg-x11-Mesa-libGLU xorg-x11-Mesa-libGL
        compat-libstdc++-33 fglrx_6_8_0 libidn"
  slc4_amd64_platformSeeds="glibc glibc-32bit coreutils bash tcsh zsh pdksh perl
        tcl tk perl-Tk readline openssl ncurses XFree86-libs
        e2fsprogs krb5-libs freetype fontconfig XFree86-Mesa-libGLU
        XFree86-Mesa-libGL xorg-x11-deprecated-libs
        xorg-x11-libs xorg-x11-Mesa-libGLU xorg-x11-Mesa-libGL
        compat-libstdc++-33 fglrx_6_8_0 libidn"
  slc5_ia32_platformSeeds="glibc coreutils bash tcsh zsh perl tcl tk readline openssl ncurses e2fsprogs krb5-libs freetype
        fontconfig compat-libstdc++-33 libidn libX11 libXmu libSM libICE libXcursor
        libXext libXrandr libXft mesa-libGLU mesa-libGL e2fsprogs-libs libXi libXinerama libXft
        libXrender libXpm"
  slc5_amd64_platformSeeds="glibc coreutils bash tcsh zsh perl tcl tk readline openssl ncurses e2fsprogs krb5-libs freetype
        fontconfig compat-libstdc++-33 libidn libX11 libXmu libSM libICE libXcursor
        libXext libXrandr libXft mesa-libGLU mesa-libGL e2fsprogs-libs libXi libXinerama libXft
        libXrender libXpm"

  slc5_corei7_platformSeeds="glibc coreutils bash tcsh zsh perl tcl tk readline openssl ncurses e2fsprogs krb5-libs freetype
        fontconfig compat-libstdc++-33 libidn libX11 libXmu libSM libICE libXcursor
        libXext libXrandr libXft mesa-libGLU mesa-libGL e2fsprogs-libs libXi libXinerama libXft
        libXrender libXpm"

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

  slc6_mic_platformSeeds="glibc coreutils bash tcsh zsh perl tcl tk readline openssl ncurses e2fsprogs krb5-libs freetype compat-readline5 ncurses-libs perl-libs perl-ExtUtils-Embed
        fontconfig compat-libstdc++-33 libidn libX11 libXmu libSM libICE libXcursor
        libXext libXrandr libXft mesa-libGLU mesa-libGL e2fsprogs-libs libXi libXinerama libXft
        libXrender libXpm libcom_err"

  # Add rh5* (not SLC5) as supported distribution.
  rh5_ia32_platformSeeds=$slc5_ia32_platformSeeds
  rh5_amd64_platformSeeds=$slc5_amd64_platformSeeds

  # This bit here is needed in case we are using the old cmsos
  # which was erroneously only reporting the platform, but not the
  # architecture.
  rh5_platformSeeds=$slc5_amd64_platformSeeds
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

slc5_compPackages="compat-readline43 libXp libXtst libXt"

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
    slc5onl* )
        additionalProvides="libX11.so.6 libXext.so.6 libXft.so.2 libXpm.so.4"
    ;;
    osx* )
        additionalProvides="AGL ApplicationServices Carbon CoreFoundation
                            CoreServices OpenGL Python QuickTime Tcl Tk
                            libintl.3.dylib libperl.dylib"

    ;;
    # Required to get slc5_amd64_gcc434 work on slc6.
    slc* )
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
 echo "unsupportedSeeds=\"$unsupportedSeeds\""; \
 echo "slc4_amd64_platformSeeds=\"$slc4_amd64_platformSeeds\""; \
 echo "slc4_ia32_platformSeeds=\"$slc4_ia32_platformSeeds\""; \
 echo "slc5_ia32_platformSeeds=\"$slc5_ia32_platformSeeds\""; \
 echo "slc5_amd64_platformSeeds=\"$slc5_amd64_platformSeeds\""; \
 echo "fc18_armv7hl_platformSeeds=\"$fc18_armv7hl_platformSeeds\""; \
 echo "fc19_armv7hl_platformSeeds=\"$fc19_armv7hl_platformSeeds\""; \
 echo "fc19_aarch64_platformSeeds=\"$fc19_aarch64_platformSeeds\""; \
 echo "slc5_corei7_platformSeeds=\"$slc5_corei7_platformSeeds\""; \
 echo "slc6_amd64_platformSeeds=\"$slc6_amd64_platformSeeds\""; \
 echo "slc7_amd64_platformSeeds=\"$slc7_amd64_platformSeeds\""; \
 echo "slc7_aarch64_platformSeeds=\"$slc7_aarch64_platformSeeds\""; \
 echo "slc7_ppc64le_platformSeeds=\"$slc7_ppc64le_platformSeeds\""; \
 echo "fc22_ppc64le_platformSeeds=\"$fc22_ppc64le_platformSeeds\""; \
 echo "fc22_ppc64_platformSeeds=\"$fc22_ppc64_platformSeeds\""; \
 echo "fc24_amd64_platformSeeds=\"$fc24_amd64_platformSeeds\""; \
 echo "fc24_ppc64le_platformSeeds=\"$fc24_ppc64le_platformSeeds\""; \
 echo "fc24_ppc64_platformSeeds=\"$fc24_ppc64_platformSeeds\""; \
 echo "slc6_mic_platformSeeds=\"$slc6_mic_platformSeeds\""; \
 echo "slc5onl_ia32_platformSeeds=\"$slc5onl_ia32_platformSeeds\""; \
 echo "slc5onl_amd64_platformSeeds=\"$slc5onl_amd64_platformSeeds\""; \
 echo "rh5_ia32_platformSeeds=\"$rh5_ia32_platformSeeds\""; \
 echo "rh5_amd64_platformSeeds=\"$rh5_amd64_platformSeeds\""; \
 echo "rh5_platformSeeds=\"$rh5_platformSeeds\""; \
 echo "packageList=\"`echo $packageList`\""; \
 echo "additionalProvides=\"$additionalProvides\""; \
 echo "unsupportedProvides=\"$unsupportedProvides\""; \
 echo "defaultPkgs=\"$defaultPkgs\""; \
) > %{i}/%{cmsplatf}-driver.txt

(echo "rpm_version=$RPM_VERSION"; \
 echo "platformSeeds=\"$platformSeeds $compPackages\""; \
 echo "unsupportedSeeds=\"$unsupportedSeeds\""; \
 echo "slc4_amd64_platformSeeds=\"$slc4_amd64_platformSeeds \""; \
 echo "slc4_ia32_platformSeeds=\"$slc4_ia32_platformSeeds \""; \
 echo "slc5_ia32_platformSeeds=\"$slc5_ia32_platformSeeds $slc5_compPackages\""; \
 echo "slc5_amd64_platformSeeds=\"$slc5_amd64_platformSeeds $slc5_compPackages\""; \
 echo "fc18_armv7hl_platformSeeds=\"$fc18_armv7hl_platformSeeds\""; \
 echo "fc19_armv7hl_platformSeeds=\"$fc19_armv7hl_platformSeeds\""; \
 echo "fc19_aarch64_platformSeeds=\"$fc19_aarch64_platformSeeds\""; \
 echo "slc5_corei7_platformSeeds=\"$slc5_corei7_platformSeeds $slc5_compPackages\""; \
 echo "slc6_amd64_platformSeeds=\"$slc6_amd64_platformSeeds $slc6_compPackages\""; \
 echo "slc7_amd64_platformSeeds=\"$slc7_amd64_platformSeeds\""; \
 echo "slc7_aarch64_platformSeeds=\"$slc7_aarch64_platformSeeds\""; \
 echo "slc7_ppc64le_platformSeeds=\"$slc7_ppc64le_platformSeeds\""; \
 echo "fc22_ppc64le_platformSeeds=\"$fc22_ppc64le_platformSeeds\""; \
 echo "fc22_ppc64_platformSeeds=\"$fc22_ppc64_platformSeeds\""; \
 echo "fc24_amd64_platformSeeds=\"$fc24_amd64_platformSeeds\""; \
 echo "fc24_ppc64le_platformSeeds=\"$fc24_ppc64le_platformSeeds\""; \
 echo "fc24_ppc64_platformSeeds=\"$fc24_ppc64_platformSeeds\""; \
 echo "slc6_mic_platformSeeds=\"$slc6_mic_platformSeeds $slc6_compPackages\""; \
 echo "slc5onl_ia32_platformSeeds=\"$slc5onl_ia32_platformSeeds $slc5_compPackages\""; \
 echo "slc5onl_amd64_platformSeeds=\"$slc5onl_amd64_platformSeeds $slc5_compPackages\""; \
 echo "rh5_ia32_platformSeeds=\"$rh5_ia32_platformSeeds\""; \
 echo "rh5_amd64_platformSeeds=\"$rh5_amd64_platformSeeds\""; \
 echo "rh5_platformSeeds=\"$rh5_platformSeeds\""; \
 echo "packageList=\"`echo $packageList`\""; \
 echo "additionalProvides=\"$additionalProvides\""; \
 echo "unsupportedProvides=\"$unsupportedProvides\""; \
 echo "defaultPkgs=\"$defaultPkgs\""; \
) > %{i}/%{cmsplatf}-driver-comp.txt

# FIXME: Hack to make sure that the cms-common package is named correctly in the driver file.
# We should make sure that the $PACKAGE_CATEGORY variable is used (requires changes to cmsBuild.sh which
# I don't want to do at this point.
perl -p -i -e 's|external[+]cms-common|cms+cms-common|g' %{i}/%{cmsplatf}-driver.txt
perl -p -i -e 's|external[+]cms-common|cms+cms-common|g' %{i}/%{cmsplatf}-driver-comp.txt
# bla bla
