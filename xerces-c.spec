### RPM external xerces-c 2.8.0
%define xercesv %(echo %realversion | tr . _)
Source: http://archive.apache.org/dist/xml/xerces-c/sources/xerces-c-src_%xercesv.tar.gz 
Patch0: xerces-c-2.8.0-osx106

%prep
%setup -n xerces-c-src_%xercesv

case %cmsplatf in
  osx106_*)
%patch0 -p1
  ;;
esac

%build
export XERCESCROOT=$PWD
cd $PWD/src/xercesc
case $(uname) in
 Linux )
   ./runConfigure -P%i -plinux -cgcc -xg++ ;;
 Darwin )
   ./runConfigure -P%i -b 64 -pmacosx -cgcc -xg++ ;;
esac
make

%install
export XERCESCROOT=$PWD
cd src/xercesc
make install

# SCRAM ToolBox toolfile
mkdir -p %i/etc/scram.d
cat << \EOF_TOOLFILE >%i/etc/scram.d/%n
<doc type=BuildSystem::ToolDoc version=1.0>
<Tool name=%n version=%v>
<info url="http://xml.apache.org/xerces-c/"></info>
<lib name=xerces-c>
<Client>
 <Environment name=XERCES_C_BASE default="%i"></Environment>
 <Environment name=INCLUDE default="$XERCES_C_BASE/include"></Environment>
 <Environment name=LIBDIR default="$XERCES_C_BASE/lib"></Environment>
</Client>
</Tool>
EOF_TOOLFILE

%post
%{relocateConfig}etc/scram.d/%n
