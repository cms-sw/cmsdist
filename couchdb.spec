### RPM external couchdb 0.8.1
Source: http://mirrors.directorymix.com/apache/incubator/%n/%realversion-incubating/apache-%n-%realversion-incubating.tar.gz
Requires: gcc curl spidermonkey openssl icu4c erlang

%prep
#%setup -n %n-%{realversion}
%setup -n apache-%n-%{realversion}-incubating

%build
export PATH=$PATH:$ICU4CU_ROOT/bin:$ERLANG_ROOT/bin
./configure --prefix=%i --with-js-lib=$SPIDERMONKEY_ROOT/lib --with-js-include=$SPIDERMONKEY_ROOT/include --with-erlang=$ERLANG_ROOT/lib/erlang/usr/include
make

%install
export PATH=$PATH:$ICU4CU_ROOT/bin:$ERLANG_ROOT/bin
make install
echo "### IN INSTALL"
pwd
find . -name couchdb
ls %i/bin/couchdb

echo $ICU4CU_ROOT

# Modify couchdb script to use env. variables rather then full path
cat %i/bin/couchdb | sed "s,$ICU4CU_ROOT,\\$ICU4CU_ROOT,g" \
        > %i/bin/couchdb.new
cat %i/bin/couchdb.new | sed "s,$ERLANG_ROOT,\\$ERLANG_ROOT,g" \
        > %i/bin/couchdb
rm -f %i/bin/couchdb.new
   
# SCRAM ToolBox toolfile
mkdir -p %i/etc/scram.d
cat << \EOF_TOOLFILE >%i/etc/scram.d/%n
<doc type=BuildSystem::ToolDoc version=1.0>
<Tool name=Couchdb version=%v>
<lib name=coucndb>
<client>
 <Environment name=COUCHDB_BASE default="%i"></Environment>
 <Environment name=INCLUDE default="$COUCHDB_BASE/include"></Environment>
 <Environment name=LIBDIR  default="$COUCHDB_BASE/lib"></Environment>
</client>
<Runtime name=PATH value="$COUCHDB_BASE/bin" type=path>
</Tool>
EOF_TOOLFILE

# This will generate the correct dependencies-setup.sh/dependencies-setup.csh
# using the information found in the Requires statements of the different
# specs and their dependencies.
mkdir -p %i/etc/profile.d
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

