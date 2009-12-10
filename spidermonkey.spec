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

# This will generate the correct dependencies-setup.sh/dependencies-setup.csh
# using the information found in the Requires statements of the different
# specs and their dependencies.
mkdir -p %{i}/etc/profile.d
echo '#!/bin/sh' > %{i}/etc/profile.d/dependencies-setup.sh
echo '#!/bin/tcsh' > %{i}/etc/profile.d/dependencies-setup.csh
echo requiredtools `echo %{requiredtools} | sed -e's|\s+| |;s|^\s+||'`
for tool in `echo %{requiredtools} | sed -e's|\s+| |;s|^\s+||'`
do
    case X$tool in
        Xdistcc|Xccache )
        ;;
        * )
            toolcap=`echo $tool | tr a-z- A-Z_`
            eval echo ". $`echo ${toolcap}_ROOT`/etc/profile.d/init.sh" >> %{i}/etc/profile.d/dependencies-setup.sh
            eval echo "source $`echo ${toolcap}_ROOT`/etc/profile.d/init.csh" >> %{i}/etc/profile.d/dependencies-setup.csh
        ;;
    esac
done
perl -p -i -e 's|\. /etc/profile\.d/init\.sh||' %{i}/etc/profile.d/dependencies-setup.sh
perl -p -i -e 's|source /etc/profile\.d/init\.csh||' %{i}/etc/profile.d/dependencies-setup.csh

%post
%{relocateConfig}etc/scram.d/%n
%{relocateConfig}etc/profile.d/dependencies-setup.sh
%{relocateConfig}etc/profile.d/dependencies-setup.csh
%{relocateConfig}/bin/js
%{relocateConfig}/bin/jscpucfg
%{relocateConfig}/bin/jskwgen
%{relocateConfig}/lib/libjs.so
%{relocateConfig}/lib/libjs.a
