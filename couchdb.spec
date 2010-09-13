### RPM external couchdb 1.0.1

#SourceX: hdttp://apache.mirror.testserver.li/couchdb/%{realversion}/apache-%n-%{realversion}.tar.gz
#Source0: svn://svn.apache.org/repos/asf/couchdb/tags/1.0.1
Source1: couch_cms_auth.erl
Patch0: couchdb-1.0.1-Makefile

# Although there is no technical software dependency,
# couchapp was included because all CMS applications will need it.
Requires: curl spidermonkey openssl icu4c erlang couchapp

%prep
#[ "$(md5sum %{SOURCE0} |cut -b1-32)" == "001cf286b72492617e9ffba271702a00" ]
#%setup -n apache-%n-%{realversion}
svn co http://svn.apache.org/repos/asf/couchdb/tags/1.0.1 %_builddir/apache-%n-%realversion
%patch0 -p0
cp %_sourcedir/couch_cms_auth.erl %_builddir/apache-%n-%realversion/src/couchdb

%build
export PATH=$PATH:$ICU4C_ROOT/bin:$ERLANG_ROOT/bin
cd %_builddir/apache-%n-%realversion
./bootstrap
./configure --prefix=%i --with-js-lib=$SPIDERMONKEY_ROOT/lib --with-js-include=$SPIDERMONKEY_ROOT/include --with-erlang=$ERLANG_ROOT/lib/erlang/usr/include
make

make install

# Modify couchdb script to use env. variables rather then full path
perl -p -i -e "s|$ICU4C_ROOT|\\\$ICU4C_ROOT|g;" \
           -e "s|$ERLANG_ROOT|\\\$ERLANG_ROOT|g;" \
           -e "s|%i|\\\$COUCHDB_ROOT|g;" \
	%i/bin/couchdb %i/bin/couchjs
chmod a+x %i/bin/couch*

%install
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
%{relocateConfig}etc/profile.d/dependencies-setup.sh
%{relocateConfig}etc/profile.d/dependencies-setup.csh
%{relocateConfig}etc/couchdb/default.ini

