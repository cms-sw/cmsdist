### RPM external spidermonkey 1.8.0_rc1
%define realver %(echo -n %{v}|tr _ -)
Source: http://ftp.mozilla.org/pub/mozilla.org/js/js-1.8.0-rc1.tar.gz


%prep
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
mkdir -p %i/include/{editline,fdlibm,liveconnect}
cp jsproto.tbl %i/include
cp *.h %i/include
cp Linux_All_DBG.OBJ/*.h %i/include
cp editline/*.h %i/include/editline
cp fdlibm/*.h %i/include/fdlibm
cp liveconnect/*.h %i/include/liveconnect
ln -s %i/lib/libjs.a %i/lib/libjs_static.a

# SCRAM ToolBox toolfile
mkdir -p %i/etc/scram.d
cat << \EOF_TOOLFILE >%i/etc/scram.d/%n
<doc type=BuildSystem::ToolDoc version=1.0>
<Tool name=Spidermonkey version=%{realver}>
<lib name=spidermonkey>
<client>
 <Environment name=SPIDERMONKEY_BASE default="%i"></Environment>
 <Environment name=INCLUDE default="$SPIDERMONKEY_BASE/include"></Environment>
 <Environment name=LIBDIR  default="$SPIDERMONKEY_BASE/lib"></Environment>
</client>
<Runtime name=PATH value="$SPIDERMONKEY_BASE/bin" type=path>
</Tool>
EOF_TOOLFILE

# setup dependencies environment
rm -rf %i/etc/profile.d
mkdir -p %i/etc/profile.d
for x in %pkgreqs; do
  case $x in /* ) continue ;; esac
  p=%{instroot}/%{cmsplatf}/$(echo $x | sed 's/\([^+]*\)+\(.*\)+\([A-Z0-9].*\)/\1 \2 \3/' | tr ' ' '/')
  echo ". $p/etc/profile.d/init.sh" >> %i/etc/profile.d/dependencies-setup.sh
  echo "source $p/etc/profile.d/init.csh" >> %i/etc/profile.d/dependencies-setup.csh
done


%post
%{relocateConfig}etc/scram.d/%n
%{relocateConfig}/bin/js
%{relocateConfig}/bin/jscpucfg
%{relocateConfig}/bin/jskwgen

# Commented out the following lines because the relocation was breaking the binary
# and avoing it to be recognized
#%{relocateConfig}/lib/libjs.so
#%{relocateConfig}/lib/libjs.a

# The relocation is also needed because of dependencies
%{relocateConfig}etc/profile.d/dependencies-setup.sh
%{relocateConfig}etc/profile.d/dependencies-setup.csh

