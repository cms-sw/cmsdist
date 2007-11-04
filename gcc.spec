### RPM external gcc 4.2.2-CMS18
## INITENV +PATH LD_LIBRARY_PATH %i/lib/32
## INITENV +PATH LD_LIBRARY_PATH %i/lib64
## BUILDIF case $(uname):$(uname -p) in Linux:i*86 ) true ;; Linux:x86_64 ) true ;;  Linux:ppc64 ) false ;; Darwin:* ) false ;; * ) true ;; esac
Source0: ftp://ftp.fu-berlin.de/unix/gnu/%n/%n-%realversion/%n-%realversion.tar.bz2
%define binutilsv 2.17
Source1: http://ftp.gnu.org/gnu/binutils/binutils-%binutilsv.tar.bz2

# If gcc version >= 4.0.0, we need two additional sources, for gmp and mpfr,
# and we set the fortranCompiler macro (which is going to be used by the 
# --enable-languages option of gcc's configure) to gfortran. 
# Notice that we need to build those twice: once using the system compiler
# and the using the newly built gcc.
%define gmpVersion 4.2.1
%define mpfrVersion 2.2.1
Source2: ftp://ftp.gnu.org/gnu/gmp/gmp-%{gmpVersion}.tar.bz2
Source3: http://www.mpfr.org/mpfr-%{mpfrVersion}/mpfr-%{mpfrVersion}.tar.bz2

%define cpu %(echo %cmsplatf | cut -d_ -f2)
%define gcc_major %(echo %realversion | cut -f1 -d.)
%prep
%setup -T -b 0 -n gcc-%realversion 

%if "%cmsos" == "slc4_ia32"
cat << \EOF_CONFIG_GCC >> gcc/config.gcc
# CMS patch to include gcc/config/i386/t-cms when building gcc
tm_file="$tm_file i386/cms.h"
tmake_file="$tmake_file i386/t-cms"
EOF_CONFIG_GCC

cat << \EOF_CMS_H > gcc/config/i386/cms.h
#undef ASM_SPEC
#define ASM_SPEC  "%%{v:-V} %%{Qy:} %%{!Qn:-Qy} %%{n} %%{T} %%{Ym,*} %%{Yd,*} %%{Wa,*:%%*} --32"
#undef CC1_SPEC
#define CC1_SPEC  "%%(cc1_cpu) %%{profile:-p} -m32"
#undef CC1PLUS_SPEC
#define CC1PLUS_SPEC "-m32"
#undef MULTILIB_DEFAULTS
#define MULTILIB_DEFAULTS { "m32" }
EOF_CMS_H

cat << \EOF_T_CMS > gcc/config/i386/t-cms
MULTILIB_OPTIONS = m32
MULTILIB_DIRNAMES = ../lib
MULTILIB_MATCHES = m32=m32
EOF_T_CMS
%endif

%setup -D -T -b 1 -n binutils-%binutilsv
%setup -D -T -b 2 -n gmp-%{gmpVersion}
%setup -D -T -b 3 -n mpfr-%{mpfrVersion}

%build
# Set special variables required to build 32-bit executables on 64-bit
# systems.  Note that if the architecture is SLC4/IA32, we may be on a
# 64-bit system and need to produce a 32-bit capable compiler, which
# _itself_ is a 32-bit executable.
case $(uname -m):%{cmsos} in
  *:slc4_ia32 )
    CCOPTS="-m32 -Wa,--32" ;;
  * )
    CCOPTS="" ;;
esac

# If requested, build our own binutils.  Currently the default is to use
# the system binutils.
%if "%{?use_external_binutils:set}" == "set"
 cd ../binutils-%{binutilsv}
 CC="gcc $CCOPTS" ./configure --prefix=%i
 make %makeprocesses
 make install
%endif

# Build GMP/MPFR for GCC 4.x
%define gcc4opts %{nil}
%if "%gcc_major" == "4"
cd ../gmp-%{gmpVersion}
CC="gcc $CCOPTS" ./configure --prefix=%i/tmp/gmp --disable-shared
make %makeprocesses
make install

cd ../mpfr-%{mpfrVersion}
CC="gcc $CCOPTS" ./configure --prefix=%i/tmp/mpfr --with-gmp=%i/tmp/gmp --disable-shared
make %makeprocesses
make install
%define gcc4opts --with-gmp=%i/tmp/gmp --with-mpfr=%i/tmp/mpfr
%endif

# Build the compilers
cd ../gcc-%realversion
mkdir -p obj
cd obj
CC="gcc $CCOPTS" \
../configure --prefix=%i \
  --enable-languages=c,c++,`case %v in 3.*) echo f77;; *) echo fortran;; esac` \
  %gcc4opts --enable-shared 

make %makeprocesses bootstrap

%install
cd %_builddir/gcc-%{realversion}/obj && make install
ln -s gcc %i/bin/cc
find %i/lib %i/lib32 %i/lib64 -name '*.la' -exec rm -f {} \; || true

# SCRAM ToolBox toolfile
%define compiler_ver        %(echo %realversion | sed -e "s|\\.||g")
%define compiler_ver_major   %(echo %realversion | sed -e "s|\\..*||")
mkdir -p %i/etc/scram.d
case %cmsplatf in
slc3* )
cat << \EOF_TOOLFILE >%i/etc/scram.d/cxxcompiler
<doc type=BuildSystem::ToolDoc version=1.1>
<tool name=cxxcompiler version=%v type=compiler>
<client>
 <Environment name=GCC_BASE default="%i"></Environment>
 <Environment name=GCCBINDIR default="$GCC_BASE/bin"></Environment>
 <Environment name=CXX value="$GCCBINDIR/c++"></Environment>
</client>
<Flags SCRAM_COMPILER_NAME="gcc%compiler_ver">
<Flags CCcompiler="gcc%compiler_ver_major">
<Flags MODULEFLAGS="-shared">
<Flags CXXDEBUGFLAG="-g">
<Flags CPPDEFINES="GNU_GCC">
<Flags CPPDEFINES="_GNU_SOURCE">
<Flags CXXSHAREDOBJECTFLAGS="-fPIC">
<Flags CXXFLAGS="-pedantic -ansi -pthread -pipe">
<Flags CXXFLAGS="-O2">
<Flags CXXFLAGS="-felide-constructors -fmessage-length=0 -ftemplate-depth-300">
<Flags CXXFLAGS="-Wall -Wno-non-template-friend -Wno-long-long -Wimplicit -Wreturn-type -Wunused -Wparentheses">
<Flags LDFLAGS="-Wl,-E">
<Flags CXXSHAREDFLAGS="-Wl,-E">
<Flags SHAREDSUFFIX="so">
<Flags SCRAM_LANGUAGE_TYPE="C++">
<Runtime name=GCC_EXEC_PREFIX default="$GCC_BASE/lib/gcc-lib/">
<Runtime name=LD_LIBRARY_PATH value="$GCC_BASE/lib" type=path>
<Runtime name=PATH value="$GCC_BASE/bin" type=path>
</tool>
EOF_TOOLFILE
cat << \EOF_TOOLFILE >%i/etc/scram.d/ccompiler
<doc type=BuildSystem::ToolDoc version=1.1>
<tool name=ccompiler version=%v type=compiler>
<client>
 <Environment name=GCC_BASE default="%i"></Environment>
 <Environment name=GCCBINDIR value="$GCC_BASE/bin"></Environment>
 <Environment name=CC value="$GCCBINDIR/gcc"></Environment>
</client>
<Flags CDEBUGFLAG="-g">
<Flags CSHAREDOBJECTFLAGS="-fPIC">
<Flags CFLAGS="-pthread">
<Flags CFLAGS="-O2">
<Flags LDFLAGS="-Wl,-E">
<Flags CSHAREDFLAGS="-Wl,-E">
<Flags SCRAM_COMPILER_NAME="gcc%compiler_ver">
<Flags SCRAM_LANGUAGE_TYPE="C">
</tool>
EOF_TOOLFILE
cat << \EOF_TOOLFILE >%i/etc/scram.d/f77compiler
<doc type=BuildSystem::ToolDoc version=1.1>
<tool name=f77compiler version=%v type=compiler> 
<lib name=g2c>
<lib name=m>
<client>
 <Environment name=G77_BASE default="%i"></Environment>
 <Environment name=FC default="$G77_BASE/bin/g77"></Environment>
</client>
<Flags SCRAM_COMPILER_NAME="gcc%compiler_ver">
<Flags FFLAGS="-fno-second-underscore -Wno-globals -Wunused -Wuninitialized">
<Flags FCO2Flag="-O2">
<Flags FCOPTIMISED="-O2">
<Flags FCDEBUGFLAG="-g">
<Flags FCSHAREDOBJECTFLAGS="-fPIC">
<Flags SCRAM_LANGUAGE_TYPE="FORTRAN">
</tool>
EOF_TOOLFILE
;;
slc4_ia32_gcc345 )
cat << \EOF_TOOLFILE >%i/etc/scram.d/cxxcompiler
<doc type=BuildSystem::ToolDoc version=1.1>
<tool name=cxxcompiler version=%v type=compiler>
<client>
 <Environment name=GCC_BASE default="%i"></Environment>
 <Environment name=GCCBINDIR default="$GCC_BASE/bin"></Environment>
 <Environment name=CXX value="$GCCBINDIR/c++"></Environment>
</client>
<Flags SCRAM_COMPILER_NAME="gcc%compiler_ver">
<Flags CCcompiler="gcc%compiler_ver_major">
<Flags MODULEFLAGS="-shared">
<Flags CXXDEBUGFLAG="-g">
<Flags CPPDEFINES="GNU_GCC">
<Flags CPPDEFINES="_GNU_SOURCE">
<Flags CXXSHAREDOBJECTFLAGS="-fPIC">
<Flags CXXFLAGS="-pedantic -ansi -pthread -pipe">
<Flags CXXFLAGS="-O2">
<Flags CXXFLAGS="-felide-constructors -fmessage-length=0 -ftemplate-depth-300">
<Flags CXXFLAGS="-Wall -Wno-non-template-friend -Wno-long-long -Wimplicit -Wreturn-type -Wunused -Wparentheses">
<Flags LDFLAGS="-Wl,-E">
<Flags CXXSHAREDFLAGS="-Wl,-E">
<Flags SHAREDSUFFIX="so">
<Flags SCRAM_LANGUAGE_TYPE="C++">
<Runtime name=LD_LIBRARY_PATH value="$GCC_BASE/lib" type=path>
<Runtime name=PATH value="$GCC_BASE/bin" type=path>
</tool>
EOF_TOOLFILE
cat << \EOF_TOOLFILE >%i/etc/scram.d/ccompiler
<doc type=BuildSystem::ToolDoc version=1.1>
<tool name=ccompiler version=%v type=compiler>
<client>
 <Environment name=GCC_BASE default="%i"></Environment>
 <Environment name=GCCBINDIR value="$GCC_BASE/bin"></Environment>
 <Environment name=CC value="$GCCBINDIR/gcc"></Environment>
</client>
<Flags CDEBUGFLAG="-g">
<Flags CSHAREDOBJECTFLAGS="-fPIC">
<Flags CFLAGS="-pthread">
<Flags CFLAGS="-O2">
<Flags LDFLAGS="-Wl,-E">
<Flags CSHAREDFLAGS="-Wl,-E">
<Flags SCRAM_COMPILER_NAME="gcc%compiler_ver">
<Flags SCRAM_LANGUAGE_TYPE="C">
</tool>
EOF_TOOLFILE
cat << \EOF_TOOLFILE >%i/etc/scram.d/f77compiler
<doc type=BuildSystem::ToolDoc version=1.1>
<tool name=f77compiler version=%v type=compiler>
<lib name=g2c>
<lib name=m>
<client>
 <Environment name=G77_BASE default="%i"></Environment>
 <Environment name=FC default="$G77_BASE/bin/g77"></Environment>
</client>
<Flags SCRAM_COMPILER_NAME="gcc%compiler_ver">
<Flags FFLAGS="-fno-second-underscore -Wno-globals -Wunused -Wuninitialized">
<Flags FCO2Flag="-O2">
<Flags FCOPTIMISED="-O2">
<Flags FCDEBUGFLAG="-g">
<Flags FCSHAREDOBJECTFLAGS="-fPIC">
<Flags SCRAM_LANGUAGE_TYPE="FORTRAN">
</tool>
EOF_TOOLFILE
;;
slc4_ia32_gcc4* )
cat << \EOF_TOOLFILE >%i/etc/scram.d/cxxcompiler
<doc type=BuildSystem::ToolDoc version=1.1>
<tool name=cxxcompiler version=%v type=compiler>
<client>
 <Environment name=GCC_BASE default="%i"></Environment>
 <Environment name=GCCBINDIR default="$GCC_BASE/bin"></Environment>
 <Environment name=CXX value="$GCCBINDIR/c++"></Environment>
</client>
<Flags SCRAM_COMPILER_NAME="gcc%compiler_ver">
<Flags CCcompiler="gcc%compiler_ver_major">
<Flags MODULEFLAGS="-shared">
<Flags CXXDEBUGFLAG="-g">
<Flags CPPDEFINES="GNU_GCC">
<Flags CPPDEFINES="_GNU_SOURCE">
<Flags CXXSHAREDOBJECTFLAGS="-fPIC">
<Flags CXXFLAGS="-pedantic -ansi -pthread -pipe">
<Flags CXXFLAGS="-O2">
<Flags CXXFLAGS="-felide-constructors -fmessage-length=0 -ftemplate-depth-300">
<Flags CXXFLAGS="-Wall -Wno-non-template-friend -Wno-long-long -Wimplicit -Wreturn-type -Wunused -Wparentheses">
<Flags LDFLAGS="-Wl,-E">
<Flags CXXSHAREDFLAGS="-Wl,-E">
<Flags SHAREDSUFFIX="so">
<Flags SCRAM_LANGUAGE_TYPE="C++">
<Runtime name=LD_LIBRARY_PATH value="$GCC_BASE/lib" type=path>
<Runtime name=PATH value="$GCC_BASE/bin" type=path>
</tool>
EOF_TOOLFILE
cat << \EOF_TOOLFILE >%i/etc/scram.d/ccompiler
<doc type=BuildSystem::ToolDoc version=1.1>
<tool name=ccompiler version=%v type=compiler>
<client>
 <Environment name=GCC_BASE default="%i"></Environment>
 <Environment name=GCCBINDIR value="$GCC_BASE/bin"></Environment>
 <Environment name=CC value="$GCCBINDIR/gcc"></Environment>
</client>
<Flags CDEBUGFLAG="-g">
<Flags CSHAREDOBJECTFLAGS="-fPIC">
<Flags CFLAGS="-pthread">
<Flags CFLAGS="-O2">
<Flags LDFLAGS="-Wl,-E">
<Flags CSHAREDFLAGS="-Wl,-E">
<Flags SCRAM_COMPILER_NAME="gcc%compiler_ver">
<Flags SCRAM_LANGUAGE_TYPE="C">
</tool>
EOF_TOOLFILE
cat << \EOF_TOOLFILE >%i/etc/scram.d/f77compiler
<doc type=BuildSystem::ToolDoc version=1.1>
<tool name=f77compiler version=%v type=compiler>
<lib name=gfortran>
<lib name=m>
<client>
 <Environment name=G77_BASE default="%i"></Environment>
 <Environment name=FC default="$G77_BASE/bin/gfortran"></Environment>
</client>
<Flags SCRAM_COMPILER_NAME="gcc%compiler_ver">
<Flags FFLAGS="-fno-second-underscore -Wunused -Wuninitialized">
<Flags FCO2Flag="-O2">
<Flags FCOPTIMISED="-O2">
<Flags FCDEBUGFLAG="-g">
<Flags FCSHAREDOBJECTFLAGS="-fPIC">
<Flags SCRAM_LANGUAGE_TYPE="FORTRAN">
</tool>
EOF_TOOLFILE
;;
slc4_amd64_* )
cat << \EOF_TOOLFILE >%i/etc/scram.d/cxxcompiler
<doc type=BuildSystem::ToolDoc version=1.1>
<tool name=cxxcompiler version=%v type=compiler>
<client>
 <Environment name=GCC_BASE default="%i"></Environment>
 <Environment name=GCCBINDIR default="$GCC_BASE/bin"></Environment>
 <Environment name=CXX value="$GCCBINDIR/c++"></Environment>
</client>
<Flags SCRAM_COMPILER_NAME="gcc%compiler_ver">
<Flags CCcompiler="gcc%compiler_ver_major">
<Flags MODULEFLAGS="-shared">
<Flags CXXDEBUGFLAG="-g">
<Flags CPPDEFINES="GNU_GCC">
<Flags CPPDEFINES="_GNU_SOURCE">
<Flags CXXSHAREDOBJECTFLAGS="-fPIC">
<Flags CXXFLAGS="-pedantic -ansi -pthread -pipe">
<Flags CXXFLAGS="-O2">
<Flags CXXFLAGS="-felide-constructors -fmessage-length=0 -ftemplate-depth-300">
<Flags CXXFLAGS="-Wall -Wno-non-template-friend -Wno-long-long -Wimplicit -Wreturn-type -Wunused -Wparentheses">
<Flags LDFLAGS="-Wl,-E">
<Flags CXXSHAREDFLAGS="-Wl,-E">
<Flags SHAREDSUFFIX="so">
<Flags SCRAM_LANGUAGE_TYPE="C++">
<Runtime name=LD_LIBRARY_PATH value="$GCC_BASE/lib64" type=path>
<Runtime name=PATH value="$GCC_BASE/bin" type=path>
</tool>
EOF_TOOLFILE
cat << \EOF_TOOLFILE >%i/etc/scram.d/ccompiler
<doc type=BuildSystem::ToolDoc version=1.1>
<tool name=ccompiler version=%v type=compiler>
<client>
 <Environment name=GCC_BASE default="%i"></Environment>
 <Environment name=GCCBINDIR value="$GCC_BASE/bin"></Environment>
 <Environment name=CC value="$GCCBINDIR/gcc"></Environment>
</client>
<Flags CDEBUGFLAG="-g">
<Flags CSHAREDOBJECTFLAGS="-fPIC">
<Flags CFLAGS="-pthread">
<Flags CFLAGS="-O2">
<Flags LDFLAGS="-Wl,-E">
<Flags CSHAREDFLAGS="-Wl,-E">
<Flags SCRAM_COMPILER_NAME="gcc%compiler_ver">
<Flags SCRAM_LANGUAGE_TYPE="C">
</tool>
EOF_TOOLFILE
cat << \EOF_TOOLFILE >%i/etc/scram.d/f77compiler
<doc type=BuildSystem::ToolDoc version=1.1>
<tool name=f77compiler version=%v type=compiler>
<lib name=g2c>
<lib name=m>
<client>
 <Environment name=G77_BASE default="%i"></Environment>
 <Environment name=FC default="$G77_BASE/bin/g77"></Environment>
</client>
<Flags SCRAM_COMPILER_NAME="gcc%compiler_ver">
<Flags FFLAGS="-fno-second-underscore -Wno-globals -Wunused -Wuninitialized">
<Flags FCO2Flag="-O2">
<Flags FCOPTIMISED="-O2">
<Flags FCDEBUGFLAG="-g">
<Flags FCSHAREDOBJECTFLAGS="-fPIC">
<Flags SCRAM_LANGUAGE_TYPE="FORTRAN">
</tool>
EOF_TOOLFILE
;;
osx104_ppc32_gcc40* )
cat << \EOF_TOOLFILE >%i/etc/scram.d/cxxcompiler
<doc type=BuildSystem::ToolDoc version=1.1>
<tool name=cxxcompiler version=%v type=compiler>
<client>
 <Environment name=GCC_BASE default="%i"></Environment>
 <Environment name=GCCBINDIR default="$GCC_BASE/bin"></Environment>
 <Environment name=CXX value="$GCCBINDIR/c++"></Environment>
</client>
<Flags SCRAM_COMPILER_NAME="gcc40">
<Flags CCcompiler="gcc40">
<Flags MODULEFLAGS=" ">
<Flags CXXDEBUGFLAG="-g">
<Flags CPPDEFINES="GNU_GCC">
<Flags CPPDEFINES="_GNU_SOURCE">
<Flags CXXSHAREDOBJECTFLAGS="-fPIC">
<Flags CXXFLAGS="-pedantic -ansi -pipe">
<Flags CXXFLAGS="-O2">
<Flags CXXFLAGS="-felide-constructors -fmessage-length=0 -ftemplate-depth-300">
<Flags CXXFLAGS="-Wall -Wno-non-template-friend -Wno-long-long -Wimplicit -Wreturn-type -Wunused -Wparentheses">
<Flags LDFLAGS=" ">
<Flags CXXSHAREDFLAGS="-dynamiclib -single_module">
<Flags SHAREDSUFFIX="dylib">
<Flags SCRAM_LANGUAGE_TYPE="C++">
<Runtime name=DYLD_LIBRARY_PATH value="$GCC_BASE/lib" type=path>
<Runtime name=PATH value="$GCC_BASE/bin" type=path>
</tool>
EOF_TOOLFILE
;;
esac

%post
# %{relocateConfig}lib/libg2c.la
# %{relocateConfig}lib/libstdc++.la
# %{relocateConfig}lib/libsupc++.la
# %if "%cpu" == "amd64"
# %{relocateConfig}lib64/libg2c.la
# %{relocateConfig}lib64/libstdc++.la
# %{relocateConfig}lib64/libsupc++.la
# %{relocateConfig}lib/32/libg2c.la
# %{relocateConfig}lib/32/libstdc++.la
# %{relocateConfig}lib/32/libsupc++.la
# %endif
# %if "%gcc4" == "true"
# %{relocateConfig}lib/libgfortran.la
# %{relocateConfig}lib/libgfortranbegin.la
# %endif
%{relocateConfig}etc/scram.d/cxxcompiler
%{relocateConfig}etc/scram.d/ccompiler
%{relocateConfig}etc/scram.d/f77compiler
