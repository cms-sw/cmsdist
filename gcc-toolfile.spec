### RPM cms gcc-toolfile 13.0

# gcc has a separate spec file for the generating a 
# toolfile because gcc.spec could be not build because of the 
# "--use-system-compiler" option.

Source: none

%prep
%build
%install
mkdir -p %{i}/etc/scram.d

# Determine the GCC_ROOT if "use system compiler" is used.
if [ "X$GCC_ROOT" = X ]
then
    export GCC_PATH=$(which gcc) || exit 1
    export GCC_ROOT=$(echo $GCC_PATH | sed -e 's|/bin/gcc||')
    export GCC_VERSION=$(gcc -dumpversion) || exit 1
    export G77_ROOT=$GCC_ROOT
else
    export GCC_PATH
    export GCC_ROOT
    export GCC_VERSION
    export G77_ROOT=$GCC_ROOT
fi

%ifos linux
export ARCH_FFLAGS="-cpp"
%endif
SCRAM_CXX11_ABI=1
echo '#include <string>' | g++ -x c++ -E -dM - | grep ' _GLIBCXX_USE_CXX11_ABI  *1' || SCRAM_CXX11_ABI=0
export SCRAM_CXX11_ABI
export COMPILER_VERSION=$(gcc -dumpversion)
export COMPILER_VERSION_MAJOR=$(echo $COMPILER_VERSION | cut -d'.' -f1)
export COMPILER_VERSION_MINOR=$(echo $COMPILER_VERSION | cut -d'.' -f2)

# Generic template for the toolfiles. 
# *** USE @VARIABLE@ plus associated environment variable to customize. ***
# DO NOT DUPLICATE the toolfile template.

cat << \EOF_TOOLFILE >%i/etc/scram.d/gcc-cxxcompiler.xml
  <tool name="gcc-cxxcompiler" version="@GCC_VERSION@" type="compiler">
    <client>
      <environment name="GCC_CXXCOMPILER_BASE" default="@GCC_ROOT@"/>
      <environment name="CXX" value="$GCC_CXXCOMPILER_BASE/bin/c++@COMPILER_NAME_SUFFIX@"/>
    </client>
    <flags CPPDEFINES="GNU_GCC _GNU_SOURCE @OS_CPPDEFINES@ @ARCH_CPPDEFINES@ @COMPILER_CPPDEFINES@"/>
    <flags CXXSHAREDOBJECTFLAGS="-fPIC @OS_CXXSHAREDOBJECTFLAGS@ @ARCH_CXXSHAREDOBJECTFLAGS@ @COMPILER_CXXSHAREDOBJECTFLAGS@"/>
    <flags CXXFLAGS="-O2 -pthread -pipe -Werror=main -Werror=pointer-arith"/>
    <flags CXXFLAGS="-Werror=overlength-strings -Wno-vla @OS_CXXFLAGS@ @ARCH_CXXFLAGS@ @COMPILER_CXXFLAGS@"/>
    <flags CXXFLAGS="-felide-constructors -fmessage-length=0"/>
    <flags CXXFLAGS="-Wall -Wno-non-template-friend -Wno-long-long -Wreturn-type"/>
   ￼ <flags CXXFLAGS="-Wextra -Wpessimizing-move -Wclass-memaccess"/>
   ￼ <flags CXXFLAGS="-Wno-cast-function-type -Wno-unused-but-set-parameter -Wno-ignored-qualifiers -Wno-deprecated-copy -Wno-unused-parameter"/>
    <flags CXXFLAGS="-Wunused -Wparentheses -Wno-deprecated -Werror=return-type"/>
    <flags CXXFLAGS="-Werror=missing-braces -Werror=unused-value"/>
    <flags CXXFLAGS="-Werror=address -Werror=format -Werror=sign-compare"/>
    <flags CXXFLAGS="-Werror=write-strings -Werror=delete-non-virtual-dtor"/>
    <flags CXXFLAGS="-Werror=strict-aliasing"/>
    <flags CXXFLAGS="-Werror=narrowing"/>
    <flags CXXFLAGS="-Werror=unused-but-set-variable -Werror=reorder"/>
    <flags CXXFLAGS="-Werror=unused-variable -Werror=conversion-null"/>
    <flags CXXFLAGS="-Werror=return-local-addr -Wnon-virtual-dtor"/>
    <flags CXXFLAGS="-Werror=switch -fdiagnostics-show-option"/>
    <flags CXXFLAGS="-Wno-unused-local-typedefs -Wno-attributes -Wno-psabi"/>
    <flags LDFLAGS="@OS_LDFLAGS@ @ARCH_LDFLAGS@ @COMPILER_LDFLAGS@"/>
    <flags CXXSHAREDFLAGS="@OS_SHAREDFLAGS@ @ARCH_SHAREDFLAGS@ @COMPILER_SHAREDFLAGS@"/>
    <flags LD_UNIT="@OS_LD_UNIT@ @ARCH_LD_UNIT@ @COMPILER_LD_UNIT@"/>
    <runtime name="@OS_RUNTIME_LDPATH_NAME@" value="$GCC_CXXCOMPILER_BASE/@ARCH_LIB64DIR@" type="path"/>
    <runtime name="@OS_RUNTIME_LDPATH_NAME@" value="$GCC_CXXCOMPILER_BASE/lib" type="path"/>
    <runtime name="SCRAM_CXX11_ABI" value="@SCRAM_CXX11_ABI@"/>
    <runtime name="PATH" value="$GCC_CXXCOMPILER_BASE/bin" type="path"/>
    <runtime name="GCC_RUNTIME_ASAN" value="$GCC_CXXCOMPILER_BASE/@ARCH_LIB64DIR@/libasan.so" type="path"/>
    <runtime name="GCC_RUNTIME_UBSAN" value="$GCC_CXXCOMPILER_BASE/@ARCH_LIB64DIR@/libubsan.so" type="path"/>
    <runtime name="GCC_RUNTIME_TSAN" value="$GCC_CXXCOMPILER_BASE/@ARCH_LIB64DIR@/libtsan.so" type="path"/>
    <runtime name="GCC_RUNTIME_LSAN" value="$GCC_CXXCOMPILER_BASE/@ARCH_LIB64DIR@/libasan.so" type="path"/>
    <runtime name="COMPILER_PATH"    value="@GCC_ROOT@"/>
  </tool>
EOF_TOOLFILE

cat << \EOF_TOOLFILE >%i/etc/scram.d/gcc-ccompiler.xml
  <tool name="gcc-ccompiler" version="@GCC_VERSION@" type="compiler">
    <client>
      <environment name="GCC_CCOMPILER_BASE" default="@GCC_ROOT@"/>
      <environment name="CC" value="$GCC_CCOMPILER_BASE/bin/gcc@COMPILER_NAME_SUFFIX@"/>
    </client>
    <flags CSHAREDOBJECTFLAGS="-fPIC @OS_CSHAREDOBJECTFLAGS@ @ARCH_CSHAREDOBJECTFLAGS@ @COMPILER_CSHAREDOBJECTFLAGS@"/>
    <flags CFLAGS="-O2 -pthread @OS_CFLAGS@ @ARCH_CFLAGS@ @COMPILER_CFLAGS@"/>
  </tool>
EOF_TOOLFILE

# Notice that on OSX we have a LIBDIR defined for f77compiler because gcc C++
# compiler (which comes from the system) does not know about where to find
# libgfortran. 
cat << \EOF_TOOLFILE >%i/etc/scram.d/gcc-f77compiler.xml
  <tool name="gcc-f77compiler" version="@GCC_VERSION@" type="compiler">
    <lib name="gfortran"/>
    <lib name="m"/>
    <client>
      <environment name="GCC_F77COMPILER_BASE" default="@G77_ROOT@"/>
      <environment name="FC" default="$GCC_F77COMPILER_BASE/bin/gfortran"/>
      @ARCH_FORTRAN_LIBDIR@
    </client>
    <flags FFLAGS="-fno-second-underscore -Wunused -Wuninitialized -O2 @OS_FFLAGS@ @ARCH_FFLAGS@ @COMPILER_FFLAGS@"/>
    <flags FFLAGS="-std=legacy"/>
    <flags FOPTIMISEDFLAGS="-O2 @OS_FOPTIMISEDFLAGS@ @ARCH_FOPTIMISEDFLAGS@ @COMPILER_FOPTIMISEDFLAGS@"/>
    <flags FSHAREDOBJECTFLAGS="-fPIC @OS_FSHAREDOBJECTFLAGS@ @ARCH_FSHAREDOBJECTFLAGS@ @COMPILER_FSHAREDOBJECTFLAGS@"/>
  </tool>
EOF_TOOLFILE

# GCC tool file for explicitly linking against libatomic
cat << \EOF_TOOLFILE >%i/etc/scram.d/gcc-atomic.xml
  <tool name="gcc-atomic" version="@GCC_VERSION@">
    <lib name="atomic"/>
    <client>
      <environment name="GCC_ATOMIC_BASE" default="@GCC_ROOT@"/>
    </client>
  </tool>
EOF_TOOLFILE

# GCC tool file for explicity linking gcc plugin library
cat << \EOF_TOOLFILE >%i/etc/scram.d/gcc-plugin.xml
  <tool name="gcc-plugin" version="@GCC_VERSION@">
    <lib name="cc1plugin cp1plugin"/>
    <client>
      <environment name="GCC_PLUGIN_BASE" default="@GCC_PLUGIN_DIR@"/>
      <environment name="INCLUDE"   default="$GCC_PLUGIN_BASE/include"/>
      <environment name="LIBDIR"    default="$GCC_PLUGIN_BASE"/>
    </client>
  </tool>
EOF_TOOLFILE

cat << \EOF_TOOLFILE >%i/etc/scram.d/ofast-flag.xml
  <tool name="ofast-flag" version="1.0">
    <flags CXXFLAGS="-Ofast"/>
    <ifarchitecture name="slc6_">
      <ifcompiler name="llvm">
        <flags CXXFLAGS="-fno-builtin"/>
      </ifcompiler>
    </ifarchitecture>
    <flags NO_RECURSIVE_EXPORT="1"/>
  </tool>
EOF_TOOLFILE
export GCC_PLUGIN_DIR=$(gcc -print-file-name=plugin)

# NON-empty defaults
# First of all handle OS specific options.
%ifos linux
  export OS_SHAREDFLAGS="-shared -Wl,-E"
  export OS_LDFLAGS="-Wl,-E -Wl,--hash-style=gnu"
  export OS_RUNTIME_LDPATH_NAME="LD_LIBRARY_PATH"
  export OS_CXXFLAGS="-Werror=overflow"
%endif
%ifos darwin
  export OS_SHAREDFLAGS="-shared -dynamic -single_module"
  export OS_LDFLAGS="-Wl,-commons -Wl,use_dylibs"
  export OS_RUNTIME_LDPATH_NAME="DYLD_LIBRARY_PATH"
%endif

# Then handle OS + architecture specific options (maybe we should enable more
# aggressive optimizations for amd64 as well??)
%ifos darwin
    export ARCH_CXXFLAGS="-arch x86_64"
    export ARCH_SHAREDFLAGS="-arch x86_64"
    export ARCH_LIB64DIR="lib"
    export ARCH_LD_UNIT="-r"
%else
    # For some reason on mac, some of the header do not compile if this is
    # defined.  Ignore for now.
    export ARCH_LIB64DIR="lib64"
    export ARCH_LD_UNIT="-r -z muldefs"
%endif

# Then handle compiler specific options. E.g. enable
# optimizations as they become available in gcc.
COMPILER_CXXFLAGS=

COMPILER_CXXFLAGS="$COMPILER_CXXFLAGS -std=c++1z -ftree-vectorize"
COMPILER_CXXFLAGS="$COMPILER_CXXFLAGS -Wstrict-overflow"
COMPILER_CXXFLAGS="$COMPILER_CXXFLAGS -Werror=array-bounds -Werror=format-contains-nul -Werror=type-limits"
COMPILER_CXXFLAGS="$COMPILER_CXXFLAGS -fvisibility-inlines-hidden"
COMPILER_CXXFLAGS="$COMPILER_CXXFLAGS -fno-math-errno --param vect-max-version-for-alias-checks=50"
COMPILER_CXXFLAGS="$COMPILER_CXXFLAGS -Xassembler --compress-debug-sections"

case %{cmsplatf} in
   *_amd64_*)
     COMPILER_CXXFLAGS="$COMPILER_CXXFLAGS -msse3"
   ;;
   *_aarch64_*)
    COMPILER_CXXFLAGS="$COMPILER_CXXFLAGS -fsigned-char -fsigned-bitfields"
   ;;
   *_ppc64le_*|*_ppc64_*)
    COMPILER_CXXFLAGS="$COMPILER_CXXFLAGS -fsigned-char -fsigned-bitfields -mlong-double-64"
   ;;
esac

export COMPILER_CXXFLAGS

# General substitutions
perl -p -i -e 's|\@([^@]*)\@|$ENV{$1}|g' %{i}/etc/scram.d/*.xml

%post
%{relocateConfig}etc/scram.d/*.xml
echo "GCC_TOOLFILE_ROOT='$CMS_INSTALL_PREFIX/%{pkgrel}'; export GCC_TOOLFILE_ROOT" > $RPM_INSTALL_PREFIX/%{pkgrel}/etc/profile.d/init.sh
echo "setenv GCC_TOOLFILE_ROOT '$CMS_INSTALL_PREFIX/%{pkgrel}'" > $RPM_INSTALL_PREFIX/%{pkgrel}/etc/profile.d/init.csh
