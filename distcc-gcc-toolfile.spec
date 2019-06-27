### RPM cms distcc-gcc-toolfile 2.0
Requires: distcc
Requires: gcc-toolfile

%if "%(echo %cmsos | grep osx >/dev/null && echo true)" == "true"
Requires: gfortran-macosx
%endif
Source: none

%prep
%build
%install
mkdir -p %i/etc/scram.d

export DISTCC_VERSION
export DISTCC_ROOT

mkdir -p %i/etc/scram.d
# Generic template for the toolfiles. 
# *** USE @VARIABLE@ plus associated environment variable to customize. ***
# DO NOT DUPLICATE the toolfile template.

cat << \EOF_TOOLFILE >%i/etc/scram.d/distcc-cxxcompiler.xml
  <tool name="distcc-cxxcompiler" version="@DISTCC_VERSION@" type="compiler">
    <use name="gcc-cxxcompiler"/>
    <client>
      <environment name="CXX" value="@DISTCC_ROOT@/bin/c++"/>
    </client>
  </tool>
EOF_TOOLFILE

cat << \EOF_TOOLFILE >%i/etc/scram.d/distcc-ccompiler.xml
  <tool name="distcc-ccompiler" version="@DISTCC_VERSION@" type="compiler">
    <use name="gcc-ccompiler"/>
    <client>
      <environment name="CC" value="@DISTCC_ROOT@/bin/gcc"/>
    </client>
  </tool>
EOF_TOOLFILE

cat << \EOF_TOOLFILE >%i/etc/scram.d/distcc-f77compiler.xml
  <tool name="distcc-f77compiler" version="@DISTCC_VERSION@" type="compiler">
    <use name="gcc-f77compiler"/>
    <client>
      <environment name="FC" default="@DISTCC_ROOT@/bin/gfortran"/>
    </client>
  </tool>
EOF_TOOLFILE

# General substitutions
export AT="@"
perl -p -i -e 's|\@([^@]*)\@|$ENV{$1}|g' %i/etc/scram.d/*.xml
%post
%{relocateConfig}etc/scram.d/*.xml
echo "DISTCC_GCC_TOOLFILE_ROOT='$CMS_INSTALL_PREFIX/%{pkgrel}'; export DISTCC_GCC_TOOLFILE_ROOT" > $RPM_INSTALL_PREFIX/%{pkgrel}/etc/profile.d/init.sh
echo "setenv DISTCC_GCC_TOOLFILE_ROOT '$CMS_INSTALL_PREFIX/%{pkgrel}'" > $RPM_INSTALL_PREFIX/%{pkgrel}/etc/profile.d/init.csh
# bla bla
