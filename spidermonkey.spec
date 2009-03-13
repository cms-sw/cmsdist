### RPM external spidermonkey 1.8.0-rc1
Source: http://ftp.mozilla.org/pub/mozilla.org/js/js-1.8.0-rc1.tar.gz

%prep
#%setup -n %n-%{realversion}
%setup -n js

%build
cd src
if [ `uname -m` != 'x86_64' ]; then
    LDEMULATION=elf_i386 make -f Makefile.ref
else
    make -f Makefile.ref
fi

%install
cd src
mkdir -p %i/bin
cp Linux_All_DBG.OBJ/{js,jscpucfg,jskwgen} %i/bin
mkdir -p %i/lib
cp Linux_All_DBG.OBJ/libjs* %i/lib

# SCRAM ToolBox toolfile
mkdir -p %i/etc/scram.d
cat << \EOF_TOOLFILE >%i/etc/scram.d/%n
<doc type=BuildSystem::ToolDoc version=1.0>
<Tool name=Spidermonkey version=%v>
<lib name=spidermonkey>
<client>
 <Environment name=SPIDERMONKEY_BASE default="%i"></Environment>
 <Environment name=INCLUDE default="$SPIDERMONKEY_BASE/include"></Environment>
 <Environment name=LIBDIR  default="$SPIDERMONKEY_BASE/lib"></Environment>
</client>
<Runtime name=PATH value="$SPIDERMONKEY_BASE/bin" type=path>
</Tool>
EOF_TOOLFILE

%post
%{relocateConfig}etc/scram.d/%n
%{relocateConfig}etc/profile.d/dependencies-setup.sh
%{relocateConfig}etc/profile.d/dependencies-setup.csh
%{relocateConfig}/bin/js
%{relocateConfig}/bin/jscpucfg
%{relocateConfig}/bin/jskwgen
%{relocateConfig}/lib/libjs.so
