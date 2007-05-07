### RPM external gcc 4.1.2 
## INITENV +PATH LD_LIBRARY_PATH %i/lib/32
## INITENV +PATH LD_LIBRARY_PATH %i/lib64
## BUILDIF case $(uname):$(uname -p) in Linux:i*86 ) true ;; Linux:x86_64 ) true ;;  Linux:ppc64 ) false ;; Darwin:* ) false ;; * ) true ;; esac
%define realversion %(echo %v | cut -d- -f1 )
Source0: ftp://ftp.fu-berlin.de/unix/gnu/%n/%n-%realversion/%n-%realversion.tar.bz2
%define binutilsv 2.17
Source1: http://ftp.gnu.org/gnu/binutils/binutils-%binutilsv.tar.bz2

# If gcc version >= 4.0.0, we need two additional sources, for gmp and mpfr,
# and we set the fortranCompiler macro (which is going to be used by the 
# --enable-languages option of gcc's configure) to gfortran. 
# Notice that we need to build those twice: once using the system compiler
# and the using the newly built gcc.
# I also set the convenience macro gcc4 to ease gcc detection.
%define gmpVersion 4.2.1
%define mpfrVersion 2.2.1
Source2: ftp://ftp.gnu.org/gnu/gmp/gmp-%{gmpVersion}.tar.bz2
Source3: http://www.mpfr.org/mpfr-current/mpfr-%{mpfrVersion}.tar.bz2
%if "%(echo %v | cut -f1 -d. )" == "4"
%define gcc4 true
%define firstStepFortran %{nil}
%define fortranCompiler ,fortran 
%else
%define firstStepFortran ,f77 
%define fortranCompiler ,f77
%endif


%define cpu %(echo %cmsplatf | cut -d_ -f2)
%prep
%setup -T -b 0 -n gcc-%realversion 

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

# We need to setup gmp and mpfr as well if the compiler version is >= 4.0.0.
%if "%{?gcc4:set}" == "set"
%setup -D -T -b 2 -n gmp-%{gmpVersion}
%setup -D -T -b 3 -n mpfr-%{mpfrVersion}
%endif

%build
# FIXME: --enable-__cxa_atexit can't be used with gcc 3.2.3 on RH 7.3,
# enabling it causes qt's uic to die with segmentation violation half
# way down the build of qt (projecsettings.ui or something like that;
# not the first or only call to uic).  Disabling the flag removes the
# issue, so clearly the option does not work correctly on this
# platform combination.


# The buildGCC function is an utility function to ease the creation of
# cross compilers.
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

    languages=c,c++%{fortranCompiler}

    if [ "$prefix" == "" ]
    then
        prefix=%i
    fi
    
    mkdir -p obj-$target
    cd obj-$target

    ../configure --prefix=$prefix --enable-languages=$languages \
        --enable-shared \
%if "%{gcc4}" == "true"
            --with-gmp-dir=%_builddir/gmp-%{gmpVersion} \
            --with-mpfr-dir=%_builddir/mpfr-%{mpfrVersion} \
%endif
        $targetOption \
        $hostOption 
    make %makeprocesses bootstrap
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
export PATH=%i/tmp/binutils/bin:$PATH
export LD_LIBRARY_PATH=%i/tmp/binutils/lib:$PATH

# Build gmp/mpfr
%if "%{?gcc4:set}" == "set"
cd ../gmp-%{gmpVersion}
./configure --prefix=%i/tmp/gmp --disable-shared
make %makeprocesses

cd ../mpfr-%{mpfrVersion}
./configure --prefix=%i/tmp/mpfr --with-gmp=%i/tmp/gmp --disable-shared
make %makeprocesses
%endif

# build the native platform compiler
cd ../gcc-%v
mkdir -p obj
cd obj
../configure --prefix=%i --enable-languages=c,c++%{fortranCompiler} \
%if "%{gcc4}" == "true"
                         --with-gmp-dir=%_builddir/gmp-%{gmpVersion} \
                         --with-mpfr-dir=%_builddir/mpfr-%{mpfrVersion} \
%endif
                         --enable-shared 

make %makeprocesses bootstrap
make install
cd ..

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
%if "%gcc4" == "true"
%{relocateConfig}lib/libbfd.la
%{relocateConfig}lib/libopcodes.la
%{relocateConfig}lib/libgfortran.la
%{relocateConfig}lib/libgfortranbegin.la
%endif
