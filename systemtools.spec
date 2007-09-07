### RPM virtual systemtools 1.0
Source: none

%define systemtools			sockets opengl x11 jcompiler
%define sockets_version			1.0
%define opengl_version			XFree4.2
%define x11_version			R6
### why oh why is this hardwired?? 
%ddefine jcompiler_version		1.5.0.p6-CMS8

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
slc3_* | slc4_* )
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

%post
%{relocateConfig}etc/scram.d/sockets
%{relocateConfig}etc/scram.d/opengl
%{relocateConfig}etc/scram.d/x11
%{relocateConfig}etc/scram.d/jcompiler
