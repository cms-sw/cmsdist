### RPM cms webtools 1.3.1
## INITENV +PATH PYTHONPATH %i/lib/python`echo $PYTHON_VERSION | cut -d. -f 1,2`/site-packages 
%define moduleName WEBTOOLS
%define exportName WEBTOOLS
%define cvstag V01-03-06
%define cvsserver cvs://:pserver:anonymous@cmscvs.cern.ch:2401/cvs_server/repositories/CMSSW?passwd=AA_:yZZ3e
Source: %cvsserver&strategy=checkout&module=%{moduleName}&nocache=true&export=%{exportName}&tag=-r%{cvstag}&output=/%{moduleName}.tar.gz
Requires: python cherrypy py2-cheetah yui sqlite zlib py2-pysqlite expat openssl bz2lib db4 gdbm py2-cx-oracle py2-formencode py2-pycrypto oracle beautifulsoup py2-sqlalchemy 
Provides: perl(CGI) 
Provides: perl(Crypt::CBC) 
Provides: perl(SecurityModule) 
Provides: perl(DBI)
%prep
%setup -n %{moduleName}
%build
rm -rf %i/etc/profile.d
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
%install
mkdir -p %i/etc
mkdir -p %i/bin
mkdir -p %i/lib/python`echo $PYTHON_VERSION | cut -d. -f1,2`/site-packages
rm -rf Applications Configuration
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
perl -p -i -e "s!\@RPM_INSTALL_PREFIX\@!$RPM_INSTALL_PREFIX/%pkgrel!" $RPM_INSTALL_PREFIX/%pkgrel/bin/cmsWeb


# setup approripate links and made post install procedure
. $RPM_INSTALL_PREFIX/%{pkgrel}/etc/profile.d/init.sh
if [ `hostname`=="cmswttest.cern.ch" ]; then
cat > $RPM_INSTALL_PREFIX/%{pkgrel}/lib/python`echo $PYTHON_VERSION | cut -d. -f1,2`/site-packages/Tools/SiteDBCore/security.ini << POST_EOF
[database]
dbtype = sqlite
dbname = $RPM_INSTALL_PREFIX/%{pkgrel}/lib/python`echo $PYTHON_VERSION | cut -d. -f1,2`/site-packages/Tools/SiteDBCore/sitedb.db
POST_EOF
else
if [ -n "${WEBTOOLS_CONF}" ] && [ -f ${WEBTOOLS_CONF}/sitedb/security.ini ]; then
ln -s ${WEBTOOLS_CONF}/sitedb/security.ini $RPM_INSTALL_PREFIX/%{pkgrel}/lib/python`echo $PYTHON_VERSION | cut -d. -f1,2`/site-packages/Tools/SiteDBCore/security.ini
fi
fi

