### RPM external xerces-c 2.7.0-CMS18
%define xercesv %(echo %realversion | tr . _)
Source: http://archive.apache.org/dist/xml/xerces-c/Xerces-C_%xercesv/source/xerces-c-src_%xercesv.tar.gz

%prep
%setup -n xerces-c-src_%xercesv

%build
export XERCESCROOT=$PWD
cd $PWD/src/xercesc
case $(uname) in
 Linux )
   ./runConfigure -P%i -plinux -cgcc -xg++ ;;
 Darwin )
   ./runConfigure -P%i -pmacosx -cgcc -xg++ ;;
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
