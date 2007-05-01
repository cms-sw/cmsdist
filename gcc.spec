### RPM external gcc 3.4.5
## INITENV +PATH LD_LIBRARY_PATH %i/lib/32
## INITENV +PATH LD_LIBRARY_PATH %i/lib64
## BUILDIF case $(uname):$(uname -p) in Linux:i*86 ) true ;; Linux:x86_64 ) true ;;  Linux:ppc64 ) false ;; Darwin:* ) false ;; * ) true ;; esac
Source0: ftp://ftp.fu-berlin.de/unix/gnu/%n/%n-%v/%n-%v.tar.bz2
%define binutilsv 2.17
Source1: http://ftp.gnu.org/gnu/binutils/binutils-%binutilsv.tar.bz2
%define cpu %(echo %cmsplatf | cut -d_ -f2)
%prep
%setup -T -b 0 -n gcc-%v 

%if "%cmsos" == "slc4_ia32"
cat << \EOF_CONFIG_GCC >> gcc/config.gcc
# CMS patch to include gcc/config/i386/t-cms when building gcc
tm_file="$tm_file i386/cms.h"
tmake_file="$tmake_file i386/t-cms"
EOF_CONFIG_GCC

cat << \EOF_CMS_H > gcc/config/i386/cms.h
#define ASM_SPEC  "%%{v:-V} %%{Qy:} %%{!Qn:-Qy} %%{n} %%{T} %%{Ym,*} %%{Yd,*} %%{Wa,*:%%*} --32"
#define CC1_SPEC  "%%(cc1_cpu) %%{profile:-p} -m32"
#define CC1PLUS_SPEC "-m32"
#define MULTILIB_DEFAULTS { "m32" }
EOF_CMS_H

cat << \EOF_T_CMS > gcc/config/i386/t-cms
MULTILIB_OPTIONS = m32
MULTILIB_DIRNAMES = ../lib
MULTILIB_MATCHES = m32=m32
EOF_T_CMS
%endif

#perl -p -i -e 's|SPECS = specs|SPECS = specs.install|' gcc/Makefile.in
%setup -D -T -b 1 -n binutils-%binutilsv
%build
# FIXME: --enable-__cxa_atexit can't be used with gcc 3.2.3 on RH 7.3,
# enabling it causes qt's uic to die with segmentation violation half
# way down the build of qt (projecsettings.ui or something like that;
# not the first or only call to uic).  Disabling the flag removes the
# issue, so clearly the option does not work correctly on this
# platform combination.

buildGCC () {
    target=$1
    host=$2
    prefix=$3

    if [ "X$target" != "X" ]
    then
        targetOption="--target $target"
    fi

    if [ "X$host" != "X" ]
    then
        hostOption="--host $host"
    fi

    languages=c,c++
    if [ "`echo %v | cut -d. -f 1`" == "3" ]
    then
        languages=c,c++,f77
    fi

    if [ "$prefix" == "" ]
    then
        prefix=%i
    fi
    
    mkdir -p obj-$target
    cd obj-$target
    
    ../configure --prefix=$prefix --enable-languages=$languages \
        --enable-shared \
        $targetOption \
        $hostOption 
    make CC1_SPEC="bogus" %makeprocesses bootstrap
    make install            
    cd ..
}

# create a tmp
mkdir -p %i/tmp

# build the latest/greatest binutils
mkdir -p %i/tmp/binutils
cd ../binutils-%{binutilsv}
./configure --prefix=%i/tmp/binutils
make %makeprocesses
make install

# build the native platform compiler
cd ../gcc-%v
export PATH=%i/tmp/binutils/bin:$PATH
export LD_LIBRARY_PATH=%i/tmp/binutils/lib:$PATH
buildGCC

# rebuild binutils with the new compiler
export PATH=%i/bin:$PATH
export LD_LIBRARY_PATH=%i/lib:$PATH
cd ../binutils-%binutilsv
./configure --prefix=%i
make %makeprocesses
make install
rm -fr %i/tmp


%install
#cd obj && make install
ln -s gcc %i/bin/cc
%post
%{relocateConfig}lib/libg2c.la
%{relocateConfig}lib/libstdc++.la
%{relocateConfig}lib/libsupc++.la
%if "%cpu" == "amd64"
%{relocateConfig}lib64/libg2c.la
%{relocateConfig}lib64/libstdc++.la
%{relocateConfig}lib64/libsupc++.la
%{relocateConfig}lib/32/libg2c.la
%{relocateConfig}lib/32/libstdc++.la
%{relocateConfig}lib/32/libsupc++.la
%endif
