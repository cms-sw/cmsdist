### RPM external couchdb 3.2.2
Source0: https://downloads.apache.org/couchdb/source/%{realversion}/apache-couchdb-%{realversion}.tar.gz

# Although there is no technical software dependency,
# couchapp was included because all CMS applications will need it.
Requires: curl spidermonkey icu4c erlang22 py3-cmscouchapp
BuildRequires: autotools

%prep
%setup -n apache-couchdb-%{realversion}

%build
export CURL_ROOT SPIDERMONKEY_ROOT ICU4C_ROOT ERLANG22_ROOT AUTOTOOLS_ROOT
# Patch the rebar configuration to have the correct path to icu and javascript
sed -i "s+-I/usr/include/js -I/usr/local/include/js+-I$SPIDERMONKEY_ROOT/include/js -I$ICU4C_ROOT/include+" %_builddir/apache-couchdb-%{realversion}/src/couch/rebar.config.script
sed -i "s+-L/usr/local/lib -lmozjs185+-L$SPIDERMONKEY_ROOT/lib -lmozjs185+" %_builddir/apache-couchdb-%{realversion}/src/couch/rebar.config.script
export PATH=$ERLANG22_ROOT/bin:$AUTOTOOLS_ROOT/bin:$PATH

./configure --with-curl \
            --skip-deps \
            --disable-docs

make %makeprocesses release CFLAGS="-I$GCC_ROOT/include -I$SPIDERMONKEY_ROOT/include/js -I$ICU4C_ROOT/include" LDFLAGS="-L$GCC_ROOT/lib64 -L$SPIDERMONKEY_ROOT/lib -L$ICU4C_ROOT/lib"

%install
# Notice: There is no 'make install' command for CouchDB 2.x+
echo "Copying CouchDB installation"
echo "Initial installation area"
ls -l %{i}
#ls -l %{_builddir}/apache-couchdb-%{realversion}/rel/couchdb
#ls -l %{_builddir}/apache-couchdb-%{realversion}/rel/couchdb/bin
#ls -l %{_builddir}/apache-couchdb-%{realversion}/rel/couchdb/lib
cp -R %{_builddir}/apache-couchdb-%{realversion}/rel/couchdb/* %{i}
#make %makeprocesses install
# install creates symlink which will point to build area, we'll resolve this
#rm %i/bin/couchjs
#cp %i/lib/couchdb/bin/couchjs %i/bin/
echo "Final installation area"
ls -l %{i}

# recommendations from: https://docs.couchdb.org/en/stable/install/unix.html#user-registration-and-security
#chown -R couchdb:couchdb %{i}
#find %{i} -type d -exec chmod 0770 {} \;
#chmod 0644 %{i}/etc/*

# install creates symlink which will point to build area, we'll resolve this
%define drop_files %i/{man,share/doc}

%post
%{relocateConfig}etc/profile.d/dependencies-setup.*sh
%{relocateConfig}etc/{rc.d,logrotate.d}/couchdb
%{relocateConfig}etc/couchdb/default.ini
%{relocateConfig}bin/couch*
%{relocateConfig}lib/couchdb/erlang/lib/couch-%{realversion}/ebin/couch.app
%{relocateConfig}lib/couchdb/erlang/lib/couch-%{realversion}/priv/lib/couch_icu_driver.la
