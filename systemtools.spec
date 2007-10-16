### RPM external systemtools 1.0-onl
Source: none

%if "%{?use_system_gcc:set}" == "set"
%define compilertools ccompiler cxxcompiler f77compiler jcompiler
%else
%define compilertools %jcompiler
%endif

%if "%{?online_release:set}" == "set"
#%define onlinetools curl libpng libtiff libungif mimetic mysql openssl oracle python elementtree qt xdaq xerces zlib
%define onlinetools zlib curl oracle mysql openssl xerces-c xdaq mimetic
# Define variables used in non-scram-managed tools, that would be
# normally defined in package's init.sh/csh scrips.
# Set all versions as currently found on the system.
%define compiler_version                3.4.6
## INITENV SET CXXCOMPILER_VERSION      %compiler_version
## INITENV SET CCOMPILER_VERSION        %compiler_version
## INITENV SET F77COMPILER_VERSION      %compiler_version
%define curl_version                    7.12.1
## INITENV SET CURL_VERSION             %curl_version
%define zlib_version                    1.2.1.2
## INITENV SET ZLIB_VERSION             %zlib_version
%define oracle_version			10.2.1
## INITENV SET ORACLE_VERSION           %oracle_version
## INITENV SET ORACLE_ROOT		/opt/xdaq
%define mysql_version			4.1.20
## INITENV SET MYSQL_VERSION            %mysql_version
%define openssl_version			0.9.7a
## INITENV SET OPENSSL_VERSION          %openssl_version
%define xerces_version			2.7.0
## INITENV SET XERCES_C_VERSION         %xerces_version
## INITENV SET XERCES_C_ROOT		/opt/xdaq
%define xdaq_version			3.13.0
## INITENV SET XDAQ_VERSION         	%xdaq_version
## INITENV SET XDAQ_ROOT         	/opt/xdaq
%define mimetic_version			0.9.1
## INITENV SET MIMETIC_VERSION         	%mimetic_version
%else
%define onlinetools %{nil}
%endif

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
cat << \EOF_TOOLFILE >%i/etc/scram.d/sockets
<doc type=BuildSystem::ToolDoc version=1.1>
<Tool name=Sockets version=%sockets_version>
EOF_TOOLFILE
case %cmsplatf in
slc3_* | slc4_* | slc4onl_* )
cat << \EOF_TOOLFILE >>%i/etc/scram.d/sockets
<lib name=nsl>
<lib name=crypt>
<lib name=dl>
EOF_TOOLFILE
;;
osx10* )
cat << \EOF_TOOLFILE >>%i/etc/scram.d/sockets
<lib name=dl>
EOF_TOOLFILE
;;
esac
echo "</Tool>" >>%i/etc/scram.d/sockets

# OpenGL
cat << \EOF_TOOLFILE >%i/etc/scram.d/opengl
<doc type=BuildSystem::ToolDoc version=1.1>
<Tool name=OpenGL version=%opengl_version>
<use name=X11>
<lib name=GL>
<lib name=GLU>
EOF_TOOLFILE
case %cmsplatf in
osx103* )
cat << \EOF_TOOLFILE >>%i/etc/scram.d/opengl
<Client>
 <Environment name=OPENGL_BASE default="/System/Library/Frameworks/OpenGL.framework/Versions/A"></Environment>
 <Environment name=INCLUDE default="$OPENGL_BASE/Headers"></Environment>
 <Environment name=LIBDIR default="$OPENGL_BASE/Libraries"></Environment>
</Client>
EOF_TOOLFILE
;;
esac
echo "</Tool>" >>%i/etc/scram.d/opengl 

# X11
cat << \EOF_TOOLFILE >%i/etc/scram.d/x11
<doc type=BuildSystem::ToolDoc version=1.1>
<Tool name=X11 version=%x11_version>
EOF_TOOLFILE
case %cmsplatf in
slc3_* )
cat << \EOF_TOOLFILE >>%i/etc/scram.d/x11
<Client>
 <Environment name=INCLUDE value="/usr/X11R6/include"></Environment>
 <Environment name=LIBDIR value="/usr/X11R6/lib"></Environment>
</Client>
<lib name=Xt>
<lib name=Xpm>
<lib name=X11>
<lib name=Xi>
<lib name=Xext>
<lib name=Xmu>
<lib name=ICE>
<lib name=SM>
EOF_TOOLFILE
;;
esac
cat << \EOF_TOOLFILE >>%i/etc/scram.d/x11
<use name=sockets>
</Tool>
EOF_TOOLFILE

# JCompiler
%define compiler_ver        %(echo %jcompiler_version | sed -e "s|\\.||g")
cat << \EOF_TOOLFILE >>%i/etc/scram.d/jcompiler
<doc type=BuildSystem::ToolDoc version=1.1>
<Tool name=jcompiler version=%jcompiler_version type=compiler>
<Client>
 <Environment name=JAVA_BASE></Environment>
 <Environment name=JAVAC value="$JAVA_BASE/bin/javac"></Environment>
</Client>
<Runtime name=JAVA_HOME default="$JAVA_BASE">
<flags JAVAC_="$(JAVAC)">
<flags JAVAC_o="$(JAVAC) -O">
<flags JAVAC_d="$(JAVAC) -g">
<Flags SCRAM_COMPILER_NAME="jsdk%compiler_ver">
<Flags SCRAM_LANGUAGE_TYPE="JAVA">
</Tool>
EOF_TOOLFILE

%if "%{?online_release:set}" == "set"
#cxxcompiler
cat << \EOF_TOOLFILE >%i/etc/scram.d/cxxcompiler
<doc type=BuildSystem::ToolDoc version=1.1>
<tool name=cxxcompiler version=%compiler_version type=compiler>
<client>
 <Environment name=GCC_BASE default="/usr"></Environment>
 <Environment name=GCCBINDIR default="$GCC_BASE/bin"></Environment>
 <Environment name=CXX value="$GCCBINDIR/c++"></Environment>
</client>
<Flags SCRAM_COMPILER_NAME="gcc345">
<Flags CCcompiler="gcc3">
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
</tool>
EOF_TOOLFILE
#ccompiler
cat << \EOF_TOOLFILE >%i/etc/scram.d/ccompiler
<doc type=BuildSystem::ToolDoc version=1.1>
<tool name=ccompiler version=%compiler_version type=compiler>
<client>
 <Environment name=GCC_BASE default="/usr"></Environment>
 <Environment name=GCCBINDIR value="$GCC_BASE/bin"></Environment>
 <Environment name=CC value="$GCCBINDIR/gcc"></Environment>
</client>
<Flags CDEBUGFLAG="-g">
<Flags CSHAREDOBJECTFLAGS="-fPIC">
<Flags CFLAGS="-pthread">
<Flags CFLAGS="-O2">
<Flags LDFLAGS="-Wl,-E">
<Flags CSHAREDFLAGS="-Wl,-E">
<Flags SCRAM_COMPILER_NAME="gcc345">
<Flags SCRAM_LANGUAGE_TYPE="C">
</tool>
EOF_TOOLFILE

#f77compiler
cat << \EOF_TOOLFILE >%i/etc/scram.d/f77compiler
<doc type=BuildSystem::ToolDoc version=1.1>
<tool name=f77compiler version=%compiler_version type=compiler> 
<lib name=g2c>
<lib name=m>
<client>
 <Environment name=G77_BASE default="/usr"></Environment>
 <Environment name=FC default="$G77_BASE/bin/g77"></Environment>
</client>
<Flags SCRAM_COMPILER_NAME="gcc345">
<Flags FFLAGS="-fno-second-underscore -Wno-globals -Wunused -Wuninitialized">
<Flags FCO2Flag="-O2">
<Flags FCOPTIMISED="-O2">
<Flags FCDEBUGFLAG="-g">
<Flags FCSHAREDFCOBJECTFLAGS="-fPIC">
<Flags SCRAM_LANGUAGE_TYPE="FORTRAN">
</tool>
EOF_TOOLFILE

# curl
cat << \EOF_TOOLFILE >%i/etc/scram.d/curl
<doc type=BuildSystem::ToolDoc version=1.0>
<Tool name=Curl version=%curl_version>
<lib name=curl>
<client>
 <Environment name=CURL_BASE default="/usr/"></Environment>
 <Environment name=INCLUDE default="$CURL_BASE/include"></Environment>
 <Environment name=LIBDIR  default="$CURL_BASE/lib"></Environment>
</client>
<Runtime name=PATH value="$CURL_BASE/bin" type=path>
</Tool>
EOF_TOOLFILE

#zlib
cat << \EOF_TOOLFILE >%i/etc/scram.d/zlib
<doc type=BuildSystem::ToolDoc version=1.0>
<Tool name=zlib version=%zlib_version>
<lib name=z>
<client>
 <Environment name=ZLIB_BASE default="/usr"></Environment>
 <Environment name=INCLUDE default="$ZLIB_BASE/include"></Environment>
 <Environment name=LIBDIR  default="$ZLIB_BASE/lib"></Environment>
</client>
</Tool>
EOF_TOOLFILE

#oracle
cat << \EOF_TOOLFILE >%i/etc/scram.d/oracle
<doc type=BuildSystem::ToolDoc version=1.0>
<Tool name=oracle version=%oracle_version>
<lib name=clntsh>
<lib name=occi>
<lib name=nnz10>
<Client>
 <Environment name=ORACLE_BASE default="/opt/xdaq"></Environment>
 <Environment name=ORACLE_ADMINDIR default="."> </Environment>
 <Environment name=LIBDIR value="$ORACLE_BASE/lib"></Environment>
 <Environment name=BINDIR value="$ORACLE_BASE/bin"></Environment>
 <Environment name=INCLUDE value="$ORACLE_BASE/include"></Environment>
</Client>
<use name=sockets>
<Runtime name=PATH value="$BINDIR" type=path>
<Runtime name=NLS_LANG value="american_america.WE8ISO8859P9">
<Runtime name=NLS_DATE_FORMAT value="DD-MON-FXYYYY">
<Runtime name=ORA_NLS33 default="$ORACLE_BASE/ocommon/nls/admin/data">
<Runtime name=ORACLE_HOME default="$ORACLE_BASE">
<Runtime name=TNS_ADMIN default="$ORACLE_ADMINDIR">
</Tool>
EOF_TOOLFILE

#mysql
cat << \EOF_TOOLFILE >%i/etc/scram.d/mysql
<doc type=BuildSystem::ToolDoc version=1.0>
<Tool name=mysql version=%mysql_version>
<Lib name=mysqlclient>
<Client>
 <Environment name=MYSQL_BASE default="/usr"></Environment>
 <Environment name=LIBDIR default="$MYSQL_BASE/lib/mysql"></Environment>
 <Environment name=MYSQL_BINDIR default="$MYSQL_BASE/bin"></Environment>
 <Environment name=INCLUDE default="$MYSQL_BASE/include/mysql"></Environment>
</Client>
<Runtime name=PATH value="$MYSQL_BINDIR" type=path>
</Tool>
EOF_TOOLFILE

#openssl
cat << \EOF_TOOLFILE >%i/etc/scram.d/openssl
<doc type=BuildSystem::ToolDoc version=1.0>
<Tool name=openssl version=%openssl_version>
<lib name=ssl>
<lib name=crypto>
<client>
 <Environment name=OPENSSL_BASE default="/usr"></Environment>
 <Environment name=INCLUDE default="$OPENSSL_BASE/include"></Environment>
 <Environment name=LIBDIR  default="$OPENSSL_BASE/lib"></Environment>
</client>
</Tool>
EOF_TOOLFILE

#xerces-c
cat << \EOF_TOOLFILE >%i/etc/scram.d/xerces-c
<doc type=BuildSystem::ToolDoc version=1.0>
<Tool name=xerces-c version=%xerces_version>
<info url="http://xml.apache.org/xerces-c/"></info>
<lib name=xerces-c>
<Client>
 <Environment name=XERCES_C_BASE default="/opt/xdaq"></Environment>
 <Environment name=INCLUDE default="$XERCES_C_BASE/include"></Environment>
 <Environment name=LIBDIR default="$XERCES_C_BASE/lib"></Environment>
</Client>
</Tool>
EOF_TOOLFILE

#xdaq
cat << \EOF_TOOLFILE >%i/etc/scram.d/xdaq
<doc type=BuildSystem::ToolDoc version=1.0>
<Tool name=XDAQ version=%xdaq_version>
<info url=http://home.cern.ch/xdaq></info>
<lib name=toolbox>
<lib name=xdaq>
<lib name=config>
<lib name=xoap>
<lib name=xgi>
<lib name=xdata>
<lib name=cgicc>
<lib name=log4cplus>
<lib name=xcept>
<lib name=logudpappender>
<lib name=peer>
<lib name=logxmlappender>
<lib name=asyncresolv>
<lib name=ptfifo>
<lib name=pthttp>
<lib name=pttcp>
<lib name=i2outils>
<lib name=xdaq2rc>
<Client>
<Environment name=XDAQ_BASE  default="/opt/xdaq"></Environment>
<Environment name=LIBDIR default="$XDAQ_BASE/lib"></Environment>
<Environment name=BINDIR default="$XDAQ_BASE/bin"></Environment>
<Environment name=INCLUDE default="$XDAQ_BASE/include"></Environment>
<Environment name=INCLUDE default="$XDAQ_BASE/include/linux"></Environment>
</Client>
<use name=xerces-c>
<use name=sockets>
<use name=mimetic>
<use name=uuid>
<runtime name=XDAQ_OS value="linux">
<runtime name=XDAQ_PLATFORM value="x86">
<runtime name=PATH value="$BINDIR" type=path>
<runtime name=XDAQ_ROOT value="$XDAQ_BASE">
<runtime name=XDAQ_DOCUMENT_ROOT value="$XDAQ_BASE/daq">
<flags CPPDEFINES="SOAP__ LITTLE_ENDIAN__">
<flags CPPDEFINES="linux">
</Tool>
EOF_TOOLFILE

#mimetic
cat << \EOF_TOOLFILE >%i/etc/scram.d/mimetic
<doc type=BuildSystem::ToolDoc version=1.0>
<Tool name=mimetic version=%mimetic_version>
<lib name=mimetic>
<Client>
 <Environment name=MIMETIC_BASE default="/opt/xdaq"></Environment>
 <Environment name=LIBDIR default="$MIMETIC_BASE/lib"></Environment>
 <Environment name=INCLUDE default="$MIMETIC_BASE/include"></Environment>
</Client>
</Tool>
EOF_TOOLFILE

%endif

%post
%{relocateConfig}etc/scram.d/sockets
%{relocateConfig}etc/scram.d/opengl
%{relocateConfig}etc/scram.d/x11
%{relocateConfig}etc/scram.d/jcompiler

%if "%{?online_release:set}" == "set"
%{relocateConfig}etc/scram.d/cxxcompiler
%{relocateConfig}etc/scram.d/ccompiler
%{relocateConfig}etc/scram.d/f77compiler
%{relocateConfig}etc/scram.d/curl
%{relocateConfig}etc/scram.d/zlib
%{relocateConfig}etc/scram.d/oracle
%{relocateConfig}etc/scram.d/mysql
%{relocateConfig}etc/scram.d/openssl
%{relocateConfig}etc/scram.d/xerces-c
%{relocateConfig}etc/scram.d/xdaq
%{relocateConfig}etc/scram.d/mimetic

%endif

