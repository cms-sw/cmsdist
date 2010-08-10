### RPM external onlinesystemtools 2.2
Source: none

# Here we are assuming that online release always uses system compiler:
%define compilertools jcompiler

%define onlinetools zlib curl openssl xerces-c xdaq xdaqheader mimetic oracle oracleocci
# Define variables used in non-scram-managed tools, that would be
# normally defined in package's init.sh/csh scrips.
# Set all versions as currently found on the system.
%define xdaq_root                       /opt/xdaq
%define curl_version                    7.12.1
## INITENV SET CURL_VERSION             %curl_version
%define zlib_version                    1.2.1.2
## INITENV SET ZLIB_VERSION             %zlib_version
%define oracle_version			10.2.1
## INITENV SET ORACLE_VERSION           %oracle_version
## INITENV SET ORACLE_ROOT		%xdaq_root
%define openssl_version			0.9.7e
## INITENV SET OPENSSL_VERSION          %openssl_version
%define xerces_version			2.7.0
## INITENV SET XERCES_C_VERSION         %xerces_version
## INITENV SET XERCES_C_ROOT		%xdaq_root
%define xdaq_version			3.32.1
## INITENV SET XDAQ_VERSION         	%xdaq_version
## INITENV SET XDAQ_ROOT         	%xdaq_root
%define mimetic_version			0.9.1
## INITENV SET MIMETIC_VERSION         	%mimetic_version

%define systemtools			sockets opengl x11 %compilertools %onlinetools
%define sockets_version			1.0
%define opengl_version			XFree4.2
%define x11_version			R6
### why oh why is this hardwired?? 
%define jcompiler_version		1.5.0.p6-CMS8

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
slc3_* | slc4_* | slc5_* | slc4onl_*| slc5onl_* )
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

# curl
cat << \EOF_TOOLFILE >%i/etc/scram.d/curl.xml
  <tool name="Curl" version="%curl_version">
    <lib name="curl"/>
    <client>
      <environment name="CURL_BASE" default="/usr/"/>
      <environment name="INCLUDE" default="$CURL_BASE/include"/>
    </client>
  </tool>
EOF_TOOLFILE

#zlib
cat << \EOF_TOOLFILE >%i/etc/scram.d/zlib.xml
  <tool name="zlib" version="%zlib_version">
    <lib name="z"/>
    <client>
      <environment name="ZLIB_BASE" default="/usr"/>
      <environment name="INCLUDE" default="$ZLIB_BASE/include"/>
    </client>
  </tool>
EOF_TOOLFILE


#openssl
cat << \EOF_TOOLFILE >%i/etc/scram.d/openssl.xml
  <tool name="openssl" version="%openssl_version">
    <lib name="ssl"/>
    <lib name="crypto"/>
    <client>
      <environment name="OPENSSL_BASE" default="/usr"/>
      <environment name="INCLUDE" default="$OPENSSL_BASE/include"/>
    </client>
  </tool>
EOF_TOOLFILE

#xerces-c
cat << \EOF_TOOLFILE >%i/etc/scram.d/xerces-c.xml
  <tool name="xerces-c" version="%xerces_version">
    <info url="http://xml.apache.org/xerces-c/"/>
    <lib name="xerces-c"/>
    <client>
      <environment name="XERCES_C_BASE" default="%xdaq_root"/>
      <environment name="INCLUDE" default="$XERCES_C_BASE/include"/>
      <environment name="LIBDIR" default="$XERCES_C_BASE/lib"/>
    </client>
  </tool>
EOF_TOOLFILE

#xdaq
cat << \EOF_TOOLFILE >%i/etc/scram.d/xdaq.xml
  <tool name="XDAQ" version="%xdaq_version">
    <info url="http://home.cern.ch/xdaq"/>
    <lib name="toolbox"/>
    <lib name="xdaq"/>
    <lib name="config"/>
    <lib name="xoap"/>
    <lib name="xgi"/>
    <lib name="xdata"/>
    <lib name="cgicc"/>
    <lib name="log4cplus"/>
    <lib name="xcept"/>
    <lib name="logudpappender"/>
    <lib name="peer"/>
    <lib name="logxmlappender"/>
    <lib name="asyncresolv"/>
    <lib name="ptfifo"/>
    <lib name="pthttp"/>
    <lib name="pttcp"/>
    <lib name="i2outils"/>
    <lib name="xdaq2rc"/>
    <client>
      <environment name="XDAQ_BASE" default="%xdaq_root"/>
      <environment name="LIBDIR" default="$XDAQ_BASE/lib"/>
      <environment name="BINDIR" default="$XDAQ_BASE/bin"/>
      <environment name="INCLUDE" default="$XDAQ_BASE/include"/>
      <environment name="INCLUDE" default="$XDAQ_BASE/include/linux"/>
    </client>
    <flags cppdefines="SOAP__ LITTLE_ENDIAN__"/>
    <flags cppdefines="linux"/>
    <runtime name="XDAQ_OS" value="linux"/>
    <runtime name="XDAQ_PLATFORM" value="x86"/>
    <runtime name="PATH" value="$BINDIR" type="path"/>
    <runtime name="XDAQ_ROOT" value="$XDAQ_BASE"/>
    <runtime name="XDAQ_DOCUMENT_ROOT" value="$XDAQ_BASE/daq"/>
    <use name="xerces-c"/>
    <use name="sockets"/>
    <use name="mimetic"/>
    <use name="uuid"/>
  </tool>
EOF_TOOLFILE

#xdaqheader
cat << \EOF_TOOLFILE >%i/etc/scram.d/xdaqheader.xml
  <tool name="XDAQHEADER" version="%xdaq_version">
    <info url="http://home.cern.ch/xdaq"/>
    <client>
      <environment name="XDAQHEADER_BASE" default="%xdaq_root"/>
      <environment name="INCLUDE" default="$XDAQHEADER_BASE/include"/>
    </client>
  </tool>
EOF_TOOLFILE

#mimetic
cat << \EOF_TOOLFILE >%i/etc/scram.d/mimetic.xml
  <tool name="mimetic" version="%mimetic_version">
    <lib name="mimetic"/>
    <client>
      <environment name="MIMETIC_BASE" default="%xdaq_root"/>
      <environment name="LIBDIR" default="$MIMETIC_BASE/lib"/>
      <environment name="INCLUDE" default="$MIMETIC_BASE/include"/>
    </client>
  </tool>
EOF_TOOLFILE

cat << \EOF_TOOLFILE >%i/etc/scram.d/oracle.xml
  <tool name="oracle" version="%oracle_version">
    <lib name="clntsh"/>
    <lib name="nnz10"/>
    <client>
      <environment name="ORACLE_BASE" default="%xdaq_root"/>
      <environment name="ORACLE_ADMINDIR" default="."/>
      <environment name="LIBDIR" value="$ORACLE_BASE/lib"/>
      <environment name="BINDIR" value="$ORACLE_BASE/bin"/>
      <environment name="INCLUDE" value="$ORACLE_BASE/include"/>
    </client>
    <runtime name="PATH" value="$BINDIR" type="path"/>
    <runtime name="TNS_ADMIN" default="$ORACLE_ADMINDIR"/>
    <use name="sockets"/>
  </tool>
EOF_TOOLFILE

cat << \EOF_TOOLFILE >%i/etc/scram.d/oracleocci.xml
  <tool name="oracleocci" version="%oracle_version">
    <lib name="occi"/>
    <use name="oracle"/>
  </tool>
EOF_TOOLFILE

%post
%{relocateConfig}/etc/scram.d/*.xml
