### RPM external base REV12

Requires: wmcore-db-couch mongo libxml2 libxslt pcre py2-ipython py2-lxml py2-mongoengine py2-pymongo py2-pystemmer py2-sphinx py2-yaml scons couchdb curl erlang icu4c openldap uuid mod_perl2 p5-cgi p5-apache-dbi p5-cgi-session p5-json-xs p5-clone p5-sort-key p5-mail-rfc822-address py2-pytz apache2 apache2-conf apache-ant apache-tomcat elementtree java-jdk libevent memcached mysql-deployment py2-memcached py2-setuptools py2-cjson beautifulsoup beecrypt boost-build boost bz2lib cherrypy db4 elfutils expat fakesystem gdbm gmp libjpg libpng libtiff mysql openssl oracle-env oracle p5-compress-zlib p5-crypt-blowfish p5-crypt-cbc p5-dbd-oracle p5-dbi p5-log-dispatch-filerotate p5-log-dispatch p5-log-log4perl p5-monalisa-apmon p5-params-validate p5-poe-component-child p5-poe p5-text-glob p5-time-hires p5-xml-parser py2-cheetah py2-cx-oracle py2-formencode py2-matplotlib py2-mysqldb py2-numpy py2-openid py2-pil py2-pycrypto py2-pyopenssl py2-pysqlite py2-python-dateutil py2-pyxml py2-simplejson py2-sqlalchemy py2-zsi python sqlite webtools wmcore-db-mysql wmcore-db-oracle wmcore-db-sqlite wmcore wmcore-webtools yui zlib

%prep
%build
%install
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
# The relocation is also needed because of dependencies
%{relocateConfig}etc/profile.d/dependencies-setup.sh
%{relocateConfig}etc/profile.d/dependencies-setup.csh

