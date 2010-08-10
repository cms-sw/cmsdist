### RPM external systemtools 19
Source: none

%if "%{?use_system_gcc:set}" == "set"
%define compilertools ccompiler cxxcompiler f77compiler jcompiler
%else
%define compilertools %jcompiler
%endif

%define systemtools			sockets opengl x11 %compilertools
%define sockets_version			1.0
%define opengl_version			XFree4.2
%define x11_version			R6
### why oh why is this hardwired?? 
%define jcompiler_version		1.5.0.p6-CMS18

## INITENV SET SOCKETS_VERSION		%sockets_version
## INITENV SET OPENGL_VERSION		%opengl_version
## INITENV SET X11_VERSION		%x11_version
## INITENV SET JCOMPILER_VERSION	%jcompiler_version
## INITENV SET JCOMPILER_TOOL	        java-jdk
## INITENV SET PKGTOOLS_SYSTEM_TOOLS	%systemtools

%prep
%build
%install
# SCRAM ToolBox toolfile
mkdir -p %i/etc/scram.d
# Sockets
cat << \EOF_TOOLFILE >%i/etc/scram.d/sockets.xml
  <tool name="sockets" version="%sockets_version">
EOF_TOOLFILE
case %cmsplatf in
slc3_* | slc4_* | slc4onl_* | slc5_* )
cat << \EOF_TOOLFILE >>%i/etc/scram.d/sockets.xml
    <lib name="nsl"/>
    <lib name="crypt"/>
    <lib name="dl"/>
EOF_TOOLFILE
;;
osx10* )
cat << \EOF_TOOLFILE >>%i/etc/scram.d/sockets.xml
    <lib name="dl"/>
EOF_TOOLFILE
;;
esac
echo "  </tool>" >>%i/etc/scram.d/sockets.xml

# OpenGL
cat << \EOF_TOOLFILE >%i/etc/scram.d/opengl.xml
  <tool name="opengl" version="%opengl_version">
    <lib name="GL"/>
    <lib name="GLU"/>
    <use name="x11"/>
EOF_TOOLFILE
case %cmsplatf in
osx103* )
cat << \EOF_TOOLFILE >>%i/etc/scram.d/opengl.xml
    <client>
      <environment name="OPENGL_BASE" default="/System/Library/Frameworks/OpenGL.framework/Versions/A"/>
      <environment name="INCLUDE"     default="$OPENGL_BASE/Headers"/>
      <environment name="LIBDIR"      default="$OPENGL_BASE/Libraries"/>
    </client>
EOF_TOOLFILE
;;
esac
echo "  </tool>" >>%i/etc/scram.d/opengl.xml

# X11
cat << \EOF_TOOLFILE >%i/etc/scram.d/x11.xml
  <tool name="x11" version="%x11_version">
EOF_TOOLFILE
case %cmsplatf in
slc3_* )
cat << \EOF_TOOLFILE >>%i/etc/scram.d/x11.xml
    <client>
      <environment name="INCLUDE" value="/usr/X11R6/include"/>
      <environment name="LIBDIR" value="/usr/X11R6/lib"/>
    </client>
    <lib name="Xt"/>
    <lib name="Xpm"/>
    <lib name="X11"/>
    <lib name="Xi"/>
    <lib name="Xext"/>
    <lib name="Xmu"/>
    <lib name="ICE"/>
    <lib name="SM"/>
EOF_TOOLFILE
;;
esac
cat << \EOF_TOOLFILE >>%i/etc/scram.d/x11.xml
    <use name="sockets"/>
  </tool>
EOF_TOOLFILE

# JCompiler
%define compiler_ver        %(echo %jcompiler_version | sed -e "s|\\.||g")
cat << \EOF_TOOLFILE >>%i/etc/scram.d/jcompiler.xml
  <tool name="jcompiler" version="%jcompiler_version" type="compiler">
    <client>
      <environment name="JAVA_BASE"/>
      <environment name="JAVAC" value="$JAVA_BASE/bin/javac"/>
    </client>
    <flags javac_="$(JAVAC)"/>
    <flags javac_o="$(JAVAC) -O"/>
    <flags javac_d="$(JAVAC) -g"/>
    <flags scram_compiler_name="jsdk%compiler_ver"/>
    <flags scram_language_type="JAVA"/>
    <runtime name="JAVA_HOME" default="$JAVA_BASE"/>
  </tool>
EOF_TOOLFILE

%post
%{relocateConfig}etc/scram.d/*.xml
