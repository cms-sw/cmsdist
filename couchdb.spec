### RPM external couchdb 1.1.0

# Using the svn url instead of the default release on because we need the 
# bootstrap script after patching the Makefile.am
Source0: svn://svn.apache.org/repos/asf/couchdb/tags/%realversion?scheme=https&module=couchdb&output=/apache-%n-%realversion.tgz
Source1: couch_cms_auth.erl
Patch0: couchdb-cmsauth-Makefile
Patch1: couchdb-ssl-client-cert
Patch2: couchdb-replication-timeout
Patch3: couchdb-replication-id
Patch4: couchdb-changes-timeout
Patch5: couchdb-changes-heartbeat
Patch6: couchdb-994-db-open-logic-11x
Patch7: couchdb-changes-retry
Patch8: couchdb-compaction-timeout

# Although there is no technical software dependency,
# couchapp was included because all CMS applications will need it.
Requires: curl spidermonkey openssl icu4c erlang couchapp
BuildRequires: autotools

%prep
%setup -n couchdb 
%patch0 -p0
%patch1 -p0
%patch2 -p0
%patch3 -p0
%patch4 -p0
%patch5 -p0
%patch6 -p0
%patch7 -p0
%patch8 -p0
cp %_sourcedir/couch_cms_auth.erl %_builddir/couchdb/src/couchdb
perl -p -i -e 's{\s*-L/(opt|usr)/local/lib}{}g; s{-I/(opt|usr)/local/include}{-I/no-no-no/include}g' configure.ac

%build
./bootstrap
export CURL_ROOT SPIDERMONKEY_ROOT OPENSSL_ROOT ICU4C_ROOT ERLANG_ROOT
./configure --prefix=%i --with-js-lib=$SPIDERMONKEY_ROOT/lib --with-js-include=$SPIDERMONKEY_ROOT/include --with-erlang=$ERLANG_ROOT/lib/erlang/usr/include --with-icu4c=$ICU4C_ROOT
make %makeprocesses

%install
make %makeprocesses install
%define drop_files %i/{man,share/doc}

# Generate dependencies-setup.{sh,csh} so init.{sh,csh} picks full environment.
mkdir -p %i/etc/profile.d
: > %i/etc/profile.d/dependencies-setup.sh
: > %i/etc/profile.d/dependencies-setup.csh
for tool in $(echo %{requiredtools} | sed -e's|\s+| |;s|^\s+||'); do
  root=$(echo $tool | tr a-z- A-Z_)_ROOT; eval r=\$$root
  if [ X"$r" != X ] && [ -r "$r/etc/profile.d/init.sh" ]; then
    echo "test X\$$root != X || . $r/etc/profile.d/init.sh" >> %i/etc/profile.d/dependencies-setup.sh
    echo "test X\$$root != X || source $r/etc/profile.d/init.csh" >> %i/etc/profile.d/dependencies-setup.csh
  fi
done

%post
%{relocateConfig}etc/profile.d/dependencies-setup.*sh
%{relocateConfig}etc/{rc.d,logrotate.d}/couchdb
%{relocateConfig}etc/couchdb/default.ini
%{relocateConfig}bin/couch*
%{relocateConfig}lib/couchdb/erlang/lib/couch-%realversion/ebin/couch.app
%{relocateConfig}lib/couchdb/erlang/lib/couch-%realversion/priv/lib/couch_icu_driver.la

