### RPM external couchdb15 1.6.1
Source0: http://www.interior-dsgn.com/apache/couchdb/source/%realversion/apache-couchdb-%realversion.tar.gz
Source1: couch_cms_auth.erl
Patch0: couchdb15-cmsauth-Makefile
Patch1: couchdb15-ssl-client-cert
Patch2: couchdb15-makefile-in
Patch3: couchdb15-fix-rep-streaming
Patch4: couchdb15-heartbeat-timeout

# Patch explanation
#   couchdb15-cmsauth-Makefile:
#     Builds couch_cms_auth.erl, the CMS authentication module
#   couchdb15-ssl-client-cert:
#     Passes cacert_file too for the ssl context in the replicator
#     code. Otherwise, it cannot use proxy certificates.
#   couchdb15-makefile-in:
#     Hack to work around build issue (Valentin?)
#   couchdb15-fix-rep-streaming:
#     Fixes or at least avoids the obscure bug of couch replicator
#     client where it does not process chunked requests correctly
#     when replicating from (but not to) a remote couch behind
#     a SSL (Apache) proxy. On this very specific case (which happens only
#     when replicating big documents), it seems couch is not reading
#     the very last received data in the SSL connection buffer.
#     We tell ibrowse to handle the (pace of) reading of incoming data buffer
#     instead of couch. Not clear if the bug is in couch or in ibrowse.
#   couchdb15-heartbeat-timeout:
#     Increases the heartbeat timeout. This would avoid the infamous
#     bug where couch kills itself when there's no incoming activity
#     for a while. Mostly affects idle couches like cmsweb-dev, but
#     could happen to production during weekends or periods of very
#     low activity. On Couch1.1.1, the timeout increasing was also
#     needed to survive when couch was very very busy and/or hanging
#     on I/O activity.


# Although there is no technical software dependency,
# couchapp was included because all CMS applications will need it.
Requires: curl spidermonkey openssl icu4c erlang couchapp
BuildRequires: autotools

%prep
%setup -n apache-couchdb-%realversion
%patch0 -p0
%patch1 -p0
%patch2 -p0
%patch3 -p0
%patch4 -p0
cp %_sourcedir/couch_cms_auth.erl %_builddir/apache-couchdb-%realversion/src/couchdb
perl -p -i -e 's{\s*-L/(opt|usr)/local/lib}{}g; s{-I/(opt|usr)/local/include}{-I/no-no-no/include}g' configure.ac
perl -p -i -e 's{-licuuc -licudt -licuin}{-licui18n -licuuc -licudata}g;' configure
perl -p -i -e 's{-licuuc -licudt -licuin}{-licui18n -licuuc -licudata}g;' configure.ac

%build
# apache 1.5.1 does not have option to specify --with-icu4c, instead
# they used --with-win32-icu-binaries which mostly the same
export CURL_ROOT SPIDERMONKEY_ROOT OPENSSL_ROOT ICU4C_ROOT ERLANG_ROOT AUTOTOOLS_ROOT
export PATH=$ERLANG_ROOT/bin:$AUTOTOOLS_ROOT/bin:$PATH
export ACLOCAL=$AUTOTOOLS_ROOT/bin/aclocal
export AUTOCONF=$AUTOTOOLS_ROOT/bin/autoconf
export AUTOMAKE=$AUTOTOOLS_ROOT/bin/automake
export AUTOHEADER=$AUTOTOOLS_ROOT/bin/autoheader
./configure --prefix=%i --with-js-lib=$SPIDERMONKEY_ROOT/lib --with-js-include=$SPIDERMONKEY_ROOT/include/js --with-erlang=$ERLANG_ROOT/lib/erlang/usr/include --with-win32-icu-binaries=$ICU4C_ROOT
make %makeprocesses

%install
make %makeprocesses install
# install creates symlink which will point to build area, we'll resolve this
rm %i/bin/couchjs
cp %i/lib/couchdb/bin/couchjs %i/bin/
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
