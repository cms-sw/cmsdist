### RPM external onlinesystemtools 3.2
## NOCOMPILER
Source: none
Requires: oracle-env

%define compilertools %{nil}
%define onlinetools zlib xerces-c xdaq xdaqheader mimetic oracle oracleocci
# Define variables used in non-scram-managed tools, that would be
# normally defined in package's init.sh/csh scrips.
# Set all versions as currently found on the system.
%define xdaq_root                       /opt/xdaq
%define zlib_version                    1.2.3
## INITENV SETV ZLIB_VERSION            %zlib_version
%define zlib_root                       /usr
## INITENV SETV ZLIB_ROOT               %zlib_root
%define libuuid_version                    1.39
## INITENV SETV LIBUUID_VERSION            %libuuid_version
%define libuuid_root                       /usr
## INITENV SETV LIBUUID_ROOT               %libuuid_root
%define sqlite_version                  3.7.5
## INITENV SETV SQLITE_VERSION          %sqlite_version
%define oracle_version                  11.2.2
## INITENV SETV ORACLE_VERSION          %oracle_version
## INITENV SETV ORACLE_ROOT             %xdaq_root
%define xerces_version                  2.8.0
## INITENV SETV XERCES_C_VERSION        %xerces_version
## INITENV SETV XERCES_C_ROOT           %xdaq_root
%define xdaq_version                    3.34.2
## INITENV SETV XDAQ_VERSION            %xdaq_version
## INITENV SETV XDAQ_ROOT               %xdaq_root
%define mimetic_version                 0.9.6
## INITENV SETV MIMETIC_VERSION         %mimetic_version

%define systemtools                     sockets opengl x11 %compilertools %onlinetools
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
case %cmsplatf in
slc4_* | slc4onl_* | slc5_* | slc5onl_* )
cat << \EOF_TOOLFILE >>%i/etc/scram.d/sockets.xml
    <lib name="nsl"/>
    <lib name="crypt"/>
    <lib name="dl"/>
    <lib name="rt"/>
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
    <environment name="ORACLE_ADMINDIR" default="@ORACLE_ENV_ROOT@/etc"/>
EOF_TOOLFILE
case %cmsplatf in
osx* )
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
osx* )
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
;;
esac
cat << \EOF_TOOLFILE >>%i/etc/scram.d/x11.xml
    <use name="sockets"/>
  </tool>
EOF_TOOLFILE

# zlib
cat << \EOF_TOOLFILE >%i/etc/scram.d/zlib.xml
  <tool name="zlib" version="%zlib_version">
    <lib name="z"/>
    <client>
      <environment name="ZLIB_BASE" default="%zlib_root"/>
      <environment name="INCLUDE" default="$ZLIB_BASE/include"/>
    </client>
  </tool>
EOF_TOOLFILE

# xerces-c
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

# xdaq
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
    <use name="libuuid"/>
  </tool>
EOF_TOOLFILE

# xdaqheader
cat << \EOF_TOOLFILE >%i/etc/scram.d/xdaqheader.xml
  <tool name="XDAQHEADER" version="%xdaq_version">
    <info url="http://home.cern.ch/xdaq"/>
    <client>
      <environment name="XDAQHEADER_BASE" default="%xdaq_root"/>
      <environment name="INCLUDE" default="$XDAQHEADER_BASE/include"/>
    </client>
  </tool>
EOF_TOOLFILE

# mimetic
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

# uuid (from e2fsprogs-libs)
cat << \EOF_TOOLFILE >%i/etc/scram.d/libuuid.xml
  <tool name="libuuid" version="%libuuid_version">
    <lib name="uuid"/>
    <client>
      <environment name="LIBUUID_BASE" default="%libuuid_root"/>
      <environment name="LIBDIR" default="$LIBUUID_BASE/lib64"/>
      <environment name="INCLUDE" default="$LIBUUID_BASE/include"/>
    </client>
    <use name="sockets"/>
  </tool>
EOF_TOOLFILE

# sqlite
cat << \EOF_TOOLFILE >%i/etc/scram.d/sqlite.xml
  <tool name="sqlite" version="%sqlite_version">
    <lib name="sqlite3"/>
    <client>
      <environment name="SQLITE_BASE" default="%xdaq_root"/>
      <environment name="LIBDIR" default="$SQLITE_BASE/lib"/>
      <environment name="BINDIR" default="$SQLITE_BASE/bin"/>
      <environment name="INCLUDE" default="$SQLITE_BASE/include"/>
    </client>
    <runtime name="PATH" value="$BINDIR" type="path"/>
  </tool>
EOF_TOOLFILE

# oracle
cat << \EOF_TOOLFILE >%i/etc/scram.d/oracle.xml
  <tool name="oracle" version="%oracle_version">
    <lib name="clntsh"/>
    <lib name="nnz11"/>
    <client>
      <environment name="ORACLE_BASE" default="%xdaq_root"/>
      <environment name="ORACLE_ADMINDIR" default="@ORACLE_ENV_ROOT@/etc"/>
      <environment name="LIBDIR" value="$ORACLE_BASE/lib"/>
      <environment name="BINDIR" value="$ORACLE_BASE/bin"/>
      <environment name="INCLUDE" value="$ORACLE_BASE/include"/>
    </client>
    <runtime name="PATH" value="$BINDIR" type="path"/>
    <runtime name="TNS_ADMIN" default="$ORACLE_ADMINDIR"/>
    <use name="sockets"/>
  </tool>
EOF_TOOLFILE

# oracleocci
cat << \EOF_TOOLFILE >%i/etc/scram.d/oracleocci.xml
  <tool name="oracleocci" version="%oracle_version">
    <lib name="occi"/>
    <use name="oracle"/>
  </tool>
EOF_TOOLFILE

export ORACLE_ENV_ROOT
perl -p -i -e 's|\@([^@]*)\@|$ENV{$1}|g' %i/etc/scram.d/*.xml

%post
%{relocateConfig}etc/scram.d/*.xml
