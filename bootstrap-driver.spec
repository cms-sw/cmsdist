### RPM external bootstrap-driver 19.0c
Source: bootstrap
Requires: apt zlib expat openssl beecrypt bz2lib db4 elfutils neon libxml2 rpm
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
    platformSeeds="glibc coreutils bash tcsh zsh pdksh perl tcl
          readline openssl ncurses
          e2fsprogs krb5-libs freetype fontconfig
          xorg-x11-deprecated-libs xorg-x11-libs xorg-x11-Mesa-libGLU
          xorg-x11-Mesa-libGL compat-libstdc++-33 libidn"
          
    # ONLINE: seed system compiler (only libraries for runtime)
    platformSeeds="$platformSeeds libgcc libstdc++"
    
    # ONLINE: seed other available system tools:
    platformSeeds="$platformSeeds curl libpng libtiff libungif openssl qt zlib perl-DBI-1.40-8"
    # Python tools are commented out due to compatibility problems.
    #platformSeeds="$platformSeeds python python-elementtree"
    
    # ONLINE: seed daq-built tools:
    platformSeeds="$platformSeeds daq-cgicc daq-mimetic daq-oracle daq-tinyproxy 
          daq-xerces daq-xdaq"
    platformSeeds="$platformSeeds daq-config daq-log4cplus daq-logudpappender 
        daq-logxmlappender daq-pt daq-ptfifo daq-pthttp 
        daq-pttcp daq-toolbox daq-xcept daq-xdaq2rc daq-xdata
        daq-xgi daq-xoap"
    ;;
*)
   platformSeeds="glibc glibc-32bit coreutils bash tcsh zsh pdksh perl
         tcl tk perl-Tk readline openssl ncurses XFree86-libs 
         e2fsprogs krb5-libs freetype fontconfig XFree86-Mesa-libGLU
         XFree86-Mesa-libGL xorg-x11-deprecated-libs
         xorg-x11-libs xorg-x11-Mesa-libGLU xorg-x11-Mesa-libGL
         compat-libstdc++-33 fglrx_6_8_0 libidn"
   ;;
esac

case $cmsplatf in
    ydl*_ppc64_* )
        platformSeeds="$platformSeeds gcc libgcc libstdc++"
    ;;
    ydl*_ppc_* )
        platformSeeds="$platformSeeds gcc libgcc libstdc++"
    ;;
esac

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
    libXft libXrender libXpm ncurses-libs"

# Case statement for additional provides.
case %cmsplatf in
    osx* )
        additionalProvides="AGL ApplicationServices Carbon CoreFoundation
                            CoreServices OpenGL Python QuickTime Tcl Tk
                            libintl.3.dylib"
    ;;
esac

unsupportedProvides="libtcl8.3.so libtk8.3.so /bin/env libcom_err.so.3 
                     libcrypto.so.4 libgssapi_krb5.so.2 libk5crypto.so.3
                     libkrb5.so.3 libssl.so.4 /bin/csh /bin/tcsh libreadline.so.4
                     libtcl8.4.so libtk8.4.so"

defaultPkgs="cms+cms-common+1.0"

mkdir -p %{i}/etc/profile.d
(echo "instroot=%{instroot}"; \
 echo "rpm_version=$RPM_VERSION"; \
 echo "apt_version=$APT_VERSION"; \
 echo "platformSeeds=\"$platformSeeds\""; \
 echo "unsupportedSeeds=\"$unsupportedSeeds\""; \
 echo "packageList=\"`echo $packageList`\""; \
 echo "additionalProvides=\"$additionalProvides\""; \
 echo "unsupportedProvides=\"$unsupportedProvides\""; \
 echo "defaultPkgs=\"$defaultPkgs\""; \
) > %{i}/%{cmsplatf}-driver.txt
# FIXME: Hack to make sure that the cms-common package is named correctly in the driver file.
# We should make sure that the $PACKAGE_CATEGORY variable is used (requires changes to cmsBuild.sh which
# I don't want to do at this point.
perl -p -i -e 's|external[+]cms-common|cms+cms-common|g' %{i}/%{cmsplatf}-driver.txt
