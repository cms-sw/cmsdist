### RPM external couchdb 1.0.1

%define svnsources http://svn.apache.org/repos/asf/couchdb/tags/%realversion
#SourceX: hdttp://apache.mirror.testserver.li/couchdb/%{realversion}/apache-%n-%{realversion}.tar.gz
Source: couch_cms_auth.erl
Patch0: couchdb-1.0.1-Makefile

# Although there is no technical software dependency,
# couchapp was included because all CMS applications will need it.
Requires: curl spidermonkey openssl icu4c erlang couchapp

%prep
#[ "$(md5sum %{SOURCE0} |cut -b1-32)" == "001cf286b72492617e9ffba271702a00" ]
#%setup -n apache-%n-%{realversion}
svn co %svnsources %_builddir/apache-%n-%realversion
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

# Generate dependencies-setup.{sh,csh} so init.{sh,csh} picks full environment.
rm -rf %i/etc/profile.d
mkdir -p %i/etc/profile.d
for tool in $(echo %{requiredtools} | sed -e's|\s+| |;s|^\s+||'); do
  root=$(echo $tool | tr a-z- A-Z_)_ROOT; eval r=\$$root
  if [ X"$r" != X ] && [ -r "$r/etc/profile.d/init.sh" ]; then
    echo "test X\$$root != X || . $r/etc/profile.d/init.sh" >> %i/etc/profile.d/dependencies-setup.sh
    echo "test X\$$root != X || source $r/etc/profile.d/init.csh" >> %i/etc/profile.d/dependencies-setup.csh
  fi
done

%post
%{relocateConfig}etc/profile.d/dependencies-setup.*sh
%{relocateConfig}etc/couchdb/default.ini

