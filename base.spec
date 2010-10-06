### RPM external base HG1010pre1

# Top level service packages
Requires: wmcore wmcore-webtools wmcore-db-sqlite wmcore-db-mysql wmcore-db-oracle wmcore-db-couch frontend webtools couchdb couchapp

# Python packages
Requires: beautifulsoup cherrypy couchapp elementtree py2-adns py2-cheetah py2-cjson py2-cx-oracle py2-formencode py2-geoip py2-httplib2 py2-ipython py2-lxml py2-matplotlib py2-memcached py2-mongoengine py2-mysqldb py2-netaddr py2-numpy py2-openid py2-pil py2-ply py2-pycrypto py2-pymongo py2-pyopenssl py2-pyrex py2-pysqlite py2-pystemmer py2-python-dateutil py2-pytz py2-pyxml py2-restkit py2-setuptools py2-simplejson py2-sphinx py2-sqlalchemy py2-yaml py2-zsi scons

# Perl packages
Requires: p5-apache2-modssl p5-apache-dbi p5-cgi p5-cgi-session p5-clone p5-compress-zlib p5-crypt-blowfish p5-crypt-cbc p5-dbd-oracle p5-dbi p5-digest-hmac p5-digest-sha1 p5-json-xs p5-log-dispatch p5-log-dispatch-filerotate p5-log-log4perl p5-mail-rfc822-address p5-monalisa-apmon p5-params-validate p5-poe p5-poe-component-child p5-poe-component-child p5-sort-key p5-text-glob p5-time-hires p5-xml-parser

# Other packages
Requires: boost boost-build erlang icu4c mongo libxslt curl libjpg libpng libtiff mysql memcached oracle oracle-env sqlite python yui zlib uuid pcre expat openssl libxml2 gmp db4 gdbm elfutils bz2lib beecrypt libevent mod_wsgi mod_perl2 apache2 apache-setup fakesystem java-jdk

# Package candidates to be removed
Requires: apache2-conf apache-ant apache-tomcat java-jdk mysql-deployment

# Removed packages
#Requires: python-ldap openldap (still needed by crab-server ?)

%prep

%build

%install
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
# The relocation below is also needed in case of dependencies
%{relocateConfig}etc/profile.d/dependencies-setup.*sh

