### RPM external systemtools 19
## NOCOMPILER
Source: none

%define islinux %(case %{cmsos} in (slc*|fc*) echo 1 ;; (*) echo 0 ;; esac)
%define isdarwin %(case %{cmsos} in (osx*) echo 1 ;; (*) echo 0 ;; esac)

%if "%{?use_system_gcc:set}" == "set"
%define compilertools ccompiler cxxcompiler f77compiler
%else
%define compilertools %{nil}
%endif

%define systemtools                     sockets opengl x11 %compilertools
%define sockets_version                 1.0
%define opengl_version                  XFree4.2
%define x11_version                     R6

## INITENV SETV SOCKETS_VERSION         %sockets_version
## INITENV SETV OPENGL_VERSION          %opengl_version
## INITENV SETV X11_VERSION             %x11_version
## INITENV SETV PKGTOOLS_SYSTEM_TOOLS   %systemtools

%prep
%build
%install
# SCRAM ToolBox toolfile
mkdir -p %i/etc/scram.d
# Sockets
cat << \EOF_TOOLFILE >%i/etc/scram.d/sockets.xml
  <tool name="sockets" version="%sockets_version">
EOF_TOOLFILE
%if %islinux
cat << \EOF_TOOLFILE >>%i/etc/scram.d/sockets.xml
    <lib name="nsl"/>
    <lib name="crypt"/>
    <lib name="dl"/>
    <lib name="rt"/>
EOF_TOOLFILE
%endif
%if %isdarwin
cat << \EOF_TOOLFILE >>%i/etc/scram.d/sockets.xml
    <lib name="dl"/>
EOF_TOOLFILE
%endif
echo "  </tool>" >>%i/etc/scram.d/sockets.xml

# OpenGL
cat << \EOF_TOOLFILE >%i/etc/scram.d/opengl.xml
  <tool name="opengl" version="%opengl_version">
    <lib name="GL"/>
    <lib name="GLU"/>
    <use name="x11"/>
    <environment name="ORACLE_ADMINDIR" default="@ORACLE_ENV_ROOT@/etc"/>
EOF_TOOLFILE
%if %isdarwin
cat << \EOF_TOOLFILE >>%i/etc/scram.d/opengl.xml
    <client>
      <environment name="OPENGL_BASE" default="/System/Library/Frameworks/OpenGL.framework/Versions/A"/>
      <environment name="INCLUDE"     default="$OPENGL_BASE/Headers"/>
      <environment name="LIBDIR"      default="$OPENGL_BASE/Libraries"/>
    </client>
EOF_TOOLFILE
%endif
echo "  </tool>" >>%i/etc/scram.d/opengl.xml

# X11
cat << \EOF_TOOLFILE >%i/etc/scram.d/x11.xml
  <tool name="x11" version="%x11_version">
EOF_TOOLFILE
%if %isdarwin
cat << \EOF_TOOLFILE >>%i/etc/scram.d/x11.xml
    <client>
      <environment name="INCLUDE" value="/usr/X11R6/include"/>
      <environment name="LIBDIR" value="/usr/X11R6/lib"/>
    </client>
    <runtime name="DYLD_FALLBACK_LIBRARY_PATH" value="$LIBDIR" type="path"/>
    <lib name="Xt"/>
    <lib name="Xpm"/>
    <lib name="X11"/>
    <lib name="Xi"/>
    <lib name="Xext"/>
    <lib name="Xmu"/>
    <lib name="ICE"/>
    <lib name="SM"/>
EOF_TOOLFILE
%endif
cat << \EOF_TOOLFILE >>%i/etc/scram.d/x11.xml
    <use name="sockets"/>
  </tool>
EOF_TOOLFILE

export ORACLE_ENV_ROOT
perl -p -i -e 's|\@([^@]*)\@|$ENV{$1}|g' %i/etc/scram.d/*.xml

%post
%{relocateConfig}etc/scram.d/*.xml
# bla bla
