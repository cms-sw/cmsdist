### RPM cms webtools 1.0.0 
## INITENV +PATH PYTHONPATH %i/lib/python`echo $PYTHON_VERSION | cut -d. -f 1,2`/site-packages 
%define moduleName WEBTOOLS
%define exportName WEBTOOLS
%define cvstag V01-00-07
%define cvsserver cvs://:pserver:anonymous@cmscvs.cern.ch:2401/cvs_server/repositories/CMSSW?passwd=AA_:yZZ3e
Source: %cvsserver&strategy=checkout&module=%{moduleName}&nocache=true&export=%{exportName}&tag=-r%{cvstag}&output=/%{moduleName}.tar.gz
Requires: python cherrypy py2-cheetah yui sqlite zlib py2-pysqlite expat openssl bz2lib db4 gdbm py2-cx-oracle py2-formencode py2-pycrypto oracle 
Provides: perl(CGI) 
Provides: perl(Crypt::CBC) 
Provides: perl(SecurityModule) 

%prep
%setup -n %{moduleName}
%build

rm -rf %i/etc/profile.d
mkdir -p %i/etc/profile.d/
dependenciesRoots="$PYTHON_ROOT $SQLITE_ROOT $PY2_PYSQLITE_ROOT $CHERRYPY_ROOT $YUI_ROOT \
                   $ZLIB_ROOT $EXPAT_ROOT $OPENSSEL_ROOT $BZ2LIB_ROOT $DB4_ROOT $GDBM_ROOT $PY2_FORMENCODE_ROOT \
                   $PY2_CHEETAH_ROOT $PY2_PYCRYPTO_ROOT $PY2_CX_ORACLE_ROOT $ORACLE_ROOT"
touch %i/etc/profile.d/dependencies-setup.csh
for pkg in $dependenciesRoots
do
    echo $pkg
    echo source $pkg/etc/profile.d/init.sh >> %i/etc/profile.d/dependencies-setup.sh
    echo source $pkg/etc/profile.d/init.csh >> %i/etc/profile.d/dependencies-setup.csh
done

python Applications/SiteDB/Utilities/CreateSiteDB.py -p `pwd`/Applications/SiteDB/

%install
mkdir -p %i/etc
mkdir -p %i/bin
mkdir -p %i/lib/python`echo $PYTHON_VERSION | cut -d. -f1,2`/site-packages
cp -r * %i/lib/python`echo $PYTHON_VERSION | cut -d. -f1,2`/site-packages
cp cmsWeb %i/bin
cat << \EOF_CHERRYPY_CONF > %i/etc/cherrypy.conf
# Serve a complete directory 
[/Common] 
tools.staticdir.on = True 
tools.staticdir.dir = %i/Common
[/Templates]
tools.staticdir.on = True
tools.staticdir.dir = %i/Templates
# Serve a complete directory 
[/WEBTOOLS/Common]
tools.staticdir.on = True
tools.staticdir.dir = %i/Common
[/WEBTOOLS/Templates]
tools.staticdir.on = True
tools.staticdir.dir = %i/Templates
EOF_CHERRYPY_CONF
cat << \EOF_APACHE2_HEADER > %i/etc/apache2-header.conf
RewriteEngine On
RewriteBase /cms/services
EOF_APACHE2_HEADER

cat << \EOF_APACHE2_CONF > %i/etc/apache2.conf
<Directory %i/Common>
Allow from all
</Directory>
<Directory %i/Templates>
Allow from all
</Directory>
EOF_APACHE2_CONF

cat << \EOF_APACHE2_FOOTER > %i/etc/apache2-footer.conf
RewriteRule ^/cms/services/webtools/Common(.*)$ %i/Common$1
RewriteRule ^/cms/services/webtools/Templates(.*)$ %i/Templates$1
EOF_APACHE2_FOOTER
%define pythonv %(echo $PYTHON_ROOT | cut -d. -f1,2)
%post
%{relocateConfig}etc/cherrypy.conf
%{relocateConfig}etc/apache2.conf
%{relocateConfig}etc/apache2-header.conf
%{relocateConfig}etc/apache2-footer.conf
%{relocateConfig}etc/profile.d/dependencies-setup.sh
%{relocateConfig}etc/profile.d/dependencies-setup.csh
%{relocateConfig}lib/python2.4/site-packages/Applications/SiteDB/sitedb.ini
perl -p -i -e "s|/BUILD/|/|;s|/WEBTOOLS/|/lib/python2.4/site-packages/|" $RPM_INSTALL_PREFIX/%pkgrel/lib/python2.4/site-packages/Applications/SiteDB/sitedb.ini
perl -p -i -e "s!\@RPM_INSTALL_PREFIX\@!$RPM_INSTALL_PREFIX/%pkgrel!" $RPM_INSTALL_PREFIX/%pkgrel/bin/cmsWeb
