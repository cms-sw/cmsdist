### RPM external bootstrap-driver 31.0
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
    zlib nss nspr popt nss-util
    automake bash bzip2 bzip2-libs bzip2-devel coreutils|coreutils-single e2fsprogs e2fsprogs-libs
    file file-libs fontconfig freetype glibc krb5-libs libaio
    libcom_err libgomp libICE
    libSM libX11 libX11-devel libxcrypt libXcursor libXext
    libXext-devel libXft libXft-devel libXi libXinerama
    libXmu libXpm libXpm-devel libXrandr libXrender
    libglvnd-opengl mesa-libGL mesa-libGLU mesa-libGLU-devel
    m4 make ncurses ncurses-libs openssl openssl-libs
    perl perl-interpreter perl-libs
    perl-Carp perl-CGI perl-constant perl-Data-Dumper
    perl-Digest-MD5 perl-Encode perl-Env perl-Exporter perl-ExtUtils-Embed
    perl-File-Path perl-File-Temp perl-Getopt-Long perl-IO perl-libnet
    perl-Memoize perl-PathTools perl-Scalar-List-Utils perl-Socket perl-Storable
    perl-Term-ANSIColor perl-Test-Harness perl-Text-ParseWords perl-Thread-Queue
    perl-Time-HiRes perl-Time-Local perl-YAML
    python2 readline rsync tcl tcsh tk wget which zsh"
  cc8_aarch64_platformSeeds="${cc8_amd64_platformSeeds}"
  cc8_aarch64_packagesWithProvides="${cc8_amd64_packagesWithProvides} libOpenGL.so.0()(64bit) libGLX.so.0()(64bit)"
  cc8_ppc64le_platformSeeds="${cc8_amd64_platformSeeds}"
  cc8_ppc64le_packagesWithProvides="${cc8_amd64_packagesWithProvides} libOpenGL.so.0()(64bit) libGLX.so.0()(64bit)"
  ;;
slc*)
  platformSeeds="glibc glibc-32bit coreutils bash tcsh zsh pdksh perl
        tcl tk perl-Tk readline openssl ncurses XFree86-libs
        e2fsprogs krb5-libs freetype fontconfig XFree86-Mesa-libGLU
        XFree86-Mesa-libGL xorg-x11-deprecated-libs
        xorg-x11-libs xorg-x11-Mesa-libGLU xorg-x11-Mesa-libGL
        compat-libstdc++-33 fglrx_6_8_0 libidn"

  slc7_common_platformSeeds="bash bzip2 bzip2-libs coreutils e2fsprogs e2fsprogs-libs file file-libs
                            fontconfig freetype gcc-c++ glibc glibc-headers hostname krb5-devel krb5-libs
                            libICE libSM libX11 libX11-devel libXcursor libXext libXext-devel libXft libXft-devel
                            libXi libXinerama libXmu libXpm libXpm-devel libXrandr libXrender libcom_err libidn
                            libstdc++ mesa-libGL mesa-libGLU mesa-libGLU-devel ncurses ncurses-libs nspr nss nss-util
                            openssl openssl-devel openssl-libs patch perl perl-Carp perl-Data-Dumper perl-Digest-MD5
                            perl-Encode perl-Env perl-Exporter perl-ExtUtils-Embed perl-ExtUtils-MakeMaker perl-File-Path
                            perl-File-Temp perl-Getopt-Long perl-PathTools perl-Socket perl-Storable perl-Switch
                            perl-Test-Harness perl-Text-ParseWords perl-Thread-Queue perl-Time-Local perl-constant
                            perl-libs perl-libwww-perl perl-threads popt readline tcl tcsh time tk zlib zsh"
  slc7_amd64_platformSeeds="${slc7_common_platformSeeds}"
  slc7_aarch64_platformSeeds="${slc7_common_platformSeeds} libGLEW glew perl-WWW-Curl texinfo perl-Module-ScanDeps"
  slc7_ppc64le_platformSeeds="${slc7_common_platformSeeds} libGLEW glew perl-WWW-Curl texinfo perl-Module-ScanDeps"
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
    cc8_* )
        additionalProvides="perl(CGI) perl(Switch)"
    ;;
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
