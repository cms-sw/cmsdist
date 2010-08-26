### RPM cms gcc-toolfile 10.0

# gcc has a separate spec file for the generating a
# toolfile because gcc.spec could be not build because of the 
# "--use-system-compiler" option.

Source: none

%prep
%build
%install
mkdir -p %i/etc/scram.d
if [ "X$GCC_ROOT" = X ]
then
    GCC_PATH=`which gcc` || exit 1
    GCC_ROOT=`echo $GCC_PATH | sed -e 's|/bin/gcc||'`
    GCC_VERSION=`gcc -v 2>&1 | grep "gcc version" | sed 's|[^0-9]*\([0-9].[0-9].[0-9]\).*|\1|'` || exit 1
fi

COMPILER_VERSION=`echo %cmsplatf | sed -e 's|.*gcc\([0-9]*\).*|\1|'`
COMPILER_VERSION_MAJOR=`echo %cmsplatf | sed -e 's|.*gcc\([0-9]\).*|\1|'`

# Generate general template for the tool files. Note that on top of
# this template there are some additional cmsplatf-dependent substitutions
# and some overall general substitutions below
case %cmsplatf in
slc5_ia32_gcc4* | slc5_amd64_gcc4* | slc5onl_ia32_gcc4* )
cat << \EOF_TOOLFILE >%i/etc/scram.d/cxxcompiler.xml
  <tool name="cxxcompiler" version="@GCC_VERSION@" type="compiler">
    <client>
      <environment name="GCC_BASE" default="@GCC_ROOT@"/>
      <environment name="GCCBINDIR" default="$GCC_BASE/bin"/>
      <environment name="CXX" value="$GCCBINDIR/c++"/>
    </client>
    <flags scram_compiler_name="gcc@COMPILER_VERSION@"/>
    <flags cccompiler="gcc@COMPILER_VERSION_MAJOR@"/>
    <flags moduleflags="-shared"/>
    <flags cxxdebugflag="-g"/>
    <flags cppdefines="GNU_GCC"/>
    <flags cppdefines="_GNU_SOURCE"/>
    <flags cxxsharedobjectflags="-fPIC"/>
    <flags cxxflags="-pedantic -ansi -pthread -pipe"/>
    <flags cxxflags="@GXXOPT@"/>
    <flags cxxflags="-felide-constructors -fmessage-length=0 -ftemplate-depth-300"/>
    <flags cxxflags="-Wall -Wno-non-template-friend -Wno-long-long -Wimplicit -Wreturn-type -Wunused -Wparentheses -Werror=array-bounds -Wno-deprecated -Werror=overflow -Werror=return-type -Werror=format-contains-nul -Werror=missing-braces -Werror=unused-value -Werror=address -Werror=format -Werror=sign-compare -Werror=write-strings -Werror=strict-overflow -fdiagnostics-show-option"/>
    <flags ldflags="@LDOPT@"/>
    <flags cxxsharedflags="-Wl,-E"/>
    <flags sharedsuffix="so"/>
    <flags scram_language_type="C++"/>
    <runtime name="LD_LIBRARY_PATH" value="$GCC_BASE/lib64" type="path" handler="warn"/>
    <runtime name="LD_LIBRARY_PATH" value="$GCC_BASE/lib" type="path"/>
    <runtime name="PATH" value="$GCC_BASE/bin" type="path"/>
  </tool>
EOF_TOOLFILE
cat << \EOF_TOOLFILE >%i/etc/scram.d/ccompiler.xml
  <tool name="ccompiler" version="@GCC_VERSION@" type="compiler">
    <client>
      <environment name="GCC_BASE" default="@GCC_ROOT@"/>
      <environment name="GCCBINDIR" value="$GCC_BASE/bin"/>
      <environment name="CC" value="$GCCBINDIR/gcc"/>
    </client>
    <flags cdebugflag="-g"/>
    <flags csharedobjectflags="-fPIC"/>
    <flags cflags="-pthread"/>
    <flags cflags="-O2"/>
    <flags ldflags="-Wl,-E"/>
    <flags csharedflags="-Wl,-E"/>
    <flags scram_compiler_name="gcc@COMPILER_VERSION@"/>
    <flags scram_language_type="C"/>
  </tool>
EOF_TOOLFILE
cat << \EOF_TOOLFILE >%i/etc/scram.d/f77compiler.xml
  <tool name="f77compiler" version="@GCC_VERSION@" type="compiler">
    <lib name="gfortran"/>
    <lib name="m"/>
    <client>
      <environment name="G77_BASE" default="@GCC_ROOT@"/>
      <environment name="FC" default="$G77_BASE/bin/gfortran"/>
    </client>
    <flags scram_compiler_name="gcc@COMPILER_VERSION@"/>
    <flags fflags="-fno-second-underscore -Wunused -Wuninitialized -O2"/>
    <flags fco2flag="-O2"/>
    <flags fcoptimised="-O2"/>
    <flags fcdebugflag="-g"/>
    <flags fcsharedobjectflags="-fPIC"/>
    <flags scram_language_type="FORTRAN"/>
  </tool>
EOF_TOOLFILE
;;
osx104_ppc32_gcc40* | osx104_ia32_gcc40* | osx10[56]*_gcc42* )
cat << \EOF_TOOLFILE >%i/etc/scram.d/cxxcompiler.xml
  <tool name="cxxcompiler" version="@GCC_VERSION@" type="compiler">
    <client>
      <environment name="GCC_BASE"  default="@GCC_ROOT@"/>
      <environment name="GCCBINDIR" default="$GCC_BASE/bin"/>
      <environment name="CXX"       value="$GCCBINDIR/c++"/>
    </client>
    <flags SCRAM_COMPILER_NAME="gcc40"/>
    <flags CCcompiler="gcc40"/>
    <flags MODULEFLAGS=" "/>
    <flags CXXDEBUGFLAG="-g"/>
    <flags CPPDEFINES="GNU_GCC"/>
    <flags CPPDEFINES="_GNU_SOURCE"/>
    <flags CXXSHAREDOBJECTFLAGS="-fPIC"/>
    <flags CXXFLAGS="@OSXARCH@ -pedantic -ansi -pipe"/>
    <flags CXXFLAGS="-O2"/>
    <flags CXXFLAGS="-felide-constructors -fmessage-length=0 -ftemplate-depth-300"/>
    <flags CXXFLAGS="-Wall -Wno-non-template-friend -Wno-long-long -Wimplicit -Wreturn-type -Wunused -Wparentheses"/>
    <flags LDFLAGS=" "/>
    <flags CXXSHAREDFLAGS="@OSXARCH@ -dynamiclib -single_module"/>
    <flags SHAREDSUFFIX="dylib"/>
    <flags SCRAM_LANGUAGE_TYPE="C++"/>
    <runtime name="DYLD_LIBRARY_PATH" value="$GCC_BASE/lib" type="path"/>
    <runtime name="PATH" value="$GCC_BASE/bin" type="path"/>
  </tool>
EOF_TOOLFILE
;;
osx10[56]*_gcc40* )
cat << \EOF_TOOLFILE >%i/etc/scram.d/cxxcompiler.xml
  <tool name="cxxcompiler" version="@GCC_VERSION@" type="compiler">
    <client>
      <environment name="GCC_BASE"  default="@GCC_ROOT@"/>
      <environment name="GCCBINDIR" default="$GCC_BASE/bin"/>
      <environment name="CXX"       value="$GCCBINDIR/c++-4.0"/>
    </client>
    <flags SCRAM_COMPILER_NAME="gcc40"/>
    <flags CCcompiler="gcc40"/>
    <flags MODULEFLAGS=" "/>
    <flags CXXDEBUGFLAG="-g"/>
    <flags CPPDEFINES="GNU_GCC"/>
    <flags CPPDEFINES="_GNU_SOURCE"/>
    <flags CXXSHAREDOBJECTFLAGS="-fPIC"/>
    <flags CXXFLAGS="@OSXARCH@ -pedantic -ansi -pipe"/>
    <flags CXXFLAGS="-O2"/>
    <flags CXXFLAGS="-felide-constructors -fmessage-length=0 -ftemplate-depth-300"/>
    <flags CXXFLAGS="-Wall -Wno-non-template-friend -Wno-long-long -Wimplicit -Wreturn-type -Wunused -Wparentheses"/>
    <flags LDFLAGS=" "/>
    <flags CXXSHAREDFLAGS="@OSXARCH@ -dynamiclib -single_module"/>
    <flags SHAREDSUFFIX="dylib"/>
    <flags SCRAM_LANGUAGE_TYPE="C++"/>
    <runtime name="DYLD_LIBRARY_PATH" value="$GCC_BASE/lib" type="path"/>
    <runtime name="PATH" value="$GCC_BASE/bin" type="path"/>
  </tool>
EOF_TOOLFILE
;;
esac

# Specific substitutions to the templates above (default case needed?)
case %cmsplatf in
  slc5_ia32_gcc4* | slc5onl_ia32_gcc4* )
    perl -p -i -e "s|\@LDOPT\@|-Wl,-E -Wl,--hash-style=gnu|g"   %i/etc/scram.d/cxxcompiler.xml
    perl -p -i -e "s|\@GXXOPT\@|-O2|g"   %i/etc/scram.d/cxxcompiler.xml
  ;;
  slc5_amd64_gcc4* )
    perl -p -i -e "s|\@LDOPT\@|-Wl,-E -Wl,--hash-style=gnu|g"   %i/etc/scram.d/cxxcompiler.xml
    perl -p -i -e "s|\@GXXOPT\@|-O2 -ftree-vectorize|g"   %i/etc/scram.d/cxxcompiler.xml
  ;;
  osx*_ia32_gcc4* )
    perl -p -i -e "s|\@OSXARCH\@|-arch i386|g"   %i/etc/scram.d/cxxcompiler.xml
  ;;
  osx*_amd64_gcc4* )
    perl -p -i -e "s|\@OSXARCH\@|-arch x86_64|g"   %i/etc/scram.d/cxxcompiler.xml
  ;;
  osx*_ppc32_gcc4* )
    perl -p -i -e "s|\@OSXARCH\@|-arch ppc|g"   %i/etc/scram.d/cxxcompiler.xml
  ;;
esac

# General substitutions
perl -p -i -e 's|\@([^@]*)\@|$ENV{$1}|g' %i/etc/scram.d/*.xml

%post
[ "X$RPM_INSTALL_PREFIX" == "X$CMS_INSTALL_PREFIX" ] || perl -p -i -e "s|$RPM_INSTALL_PREFIX|$CMS_INSTALL_PREFIX|g" $RPM_INSTALL_PREFIX/%{pkgrel}/etc/scram.d/*.xml
echo "GCC_TOOLFILE_ROOT='$CMS_INSTALL_PREFIX/%{pkgrel}'; export GCC_TOOLFILE_ROOT" > $RPM_INSTALL_PREFIX/%{pkgrel}/etc/profile.d/init.sh
echo "setenv GCC_TOOLFILE_ROOT '$CMS_INSTALL_PREFIX/%{pkgrel}'" > $RPM_INSTALL_PREFIX/%{pkgrel}/etc/profile.d/init.csh
