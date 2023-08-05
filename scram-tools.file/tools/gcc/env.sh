#!/bin/bash -e

if [ "X$GCC_ROOT" = X ]
then
    GCC_ROOT=$(which gcc | sed -e 's|/bin/gcc||')
    GCC_VERSION=$(gcc -dumpversion) || exit 1
fi
export TOOL_ROOT=$GCC_ROOT
export TOOL_VERSION=$GCC_VERSION
export GCC_PLUGIN_DIR=$(gcc -print-file-name=plugin)
SCRAM_CXX11_ABI=1
echo '#include <string>' | g++ -x c++ -E -dM - | grep ' _GLIBCXX_USE_CXX11_ABI  *1' || SCRAM_CXX11_ABI=0
export SCRAM_CXX11_ABI

# First of all handle OS specific options.
OS_LIB64DIR="lib64"
if [ $(uname -s) = "Darwin" ] ; then
  OS_SHAREDFLAGS="-shared -dynamic -single_module -arch x86_64"
  OS_LDFLAGS="-Wl,-commons -Wl,use_dylibs"
  OS_CXXFLAGS="-arch x86_64"
  OS_LIB64DIR="lib"
  OS_LD_UNIT="-r"
else
  OS_SHAREDFLAGS="-shared -Wl,-E"
  OS_LDFLAGS="-Wl,-E -Wl,--hash-style=gnu"
  OS_CXXFLAGS="-Werror=overflow"
  OS_FFLAGS="-cpp"
  OS_LD_UNIT="-r -z muldefs"
fi
export OS_LIB64DIR
source ${SCRAM_TOOLS_BIN_DIR}/os_libdir.sh

# Then handle compiler specific options. E.g. enable
# optimizations as they become available in gcc.

GCC_CXXFLAGS=""
GCC_CXXFLAGS="$GCC_CXXFLAGS -std=c++${CMS_CXX_STANDARD} -ftree-vectorize"
GCC_CXXFLAGS="$GCC_CXXFLAGS -Werror=array-bounds -Werror=format-contains-nul -Werror=type-limits"
GCC_CXXFLAGS="$GCC_CXXFLAGS -fvisibility-inlines-hidden"
GCC_CXXFLAGS="$GCC_CXXFLAGS -fno-math-errno --param vect-max-version-for-alias-checks=50"
GCC_CXXFLAGS="$GCC_CXXFLAGS -Xassembler --compress-debug-sections"

# Explicitly use the GNU binutils ld.bfd linker
GCC_CXXFLAGS="$GCC_CXXFLAGS -fuse-ld=bfd"

case $(uname -m) in
  aarch64 ) GCC_CXXFLAGS="$GCC_CXXFLAGS -fsigned-char -fsigned-bitfields" ;;
  ppc64le ) GCC_CXXFLAGS="$GCC_CXXFLAGS -fsigned-char -fsigned-bitfields" ;;
esac

#C-COMPILER
export GCC_CFLAGS="${OS_CFLAGS} ${ARCH_CFLAGS} ${GCC_CFLAGS} ${COMPILER_CFLAGS}"
export GCC_CSHAREDOBJECTFLAGS="${OS_CSHAREDOBJECTFLAGS} ${ARCH_CSHAREDOBJECTFLAGS} ${GCC_CSHAREDOBJECTFLAGS} ${COMPILER_CSHAREDOBJECTFLAGS}"

#CXX-COMPILER
export GCC_CPPDEFINES="${OS_CPPDEFINES} ${ARCH_CPPDEFINES} ${GCC_CPPDEFINES} ${COMPILER_CPPDEFINES}"
export GCC_CXXFLAGS="${OS_CXXFLAGS} ${ARCH_CXXFLAGS} ${GCC_CXXFLAGS} ${COMPILER_CXXFLAGS}"
export GCC_CXXSHAREDOBJECTFLAGS="${OS_CXXSHAREDOBJECTFLAGS} ${ARCH_CXXSHAREDOBJECTFLAGS} ${GCC_CXXSHAREDOBJECTFLAGS} ${COMPILER_CXXSHAREDOBJECTFLAGS}"
export GCC_LDFLAGS="${OS_LDFLAGS} ${ARCH_LDFLAGS} ${GCC_LDFLAGS} ${COMPILER_LDFLAGS}"
export GCC_LD_UNIT="${OS_LD_UNIT} ${ARCH_LD_UNIT} ${GCC_LD_UNIT} ${COMPILER_LD_UNIT}"
export GCC_SHAREDFLAGS="${OS_SHAREDFLAGS} ${ARCH_SHAREDFLAGS} ${GCC_SHAREDFLAGS} ${COMPILER_SHAREDFLAGS}"
export COMPILER_NAME_SUFFIX

#F77-COMPILER
export GCC_FFLAGS="${OS_FFLAGS} ${ARCH_FFLAGS} ${GCC_FFLAGS} ${COMPILER_FFLAGS}"
export GCC_FOPTIMISEDFLAGS="${OS_FOPTIMISEDFLAGS} ${ARCH_FOPTIMISEDFLAGS} ${GCC_FOPTIMISEDFLAGS} ${COMPILER_FOPTIMISEDFLAGS}"
export GCC_FSHAREDOBJECTFLAGS="${OS_FSHAREDOBJECTFLAGS} ${ARCH_FSHAREDOBJECTFLAGS} ${GCC_FSHAREDOBJECTFLAGS} ${COMPILER_FSHAREDOBJECTFLAGS}"

