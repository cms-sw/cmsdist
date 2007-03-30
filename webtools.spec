### RPM cms webtools ALPHA-cp3 
%define moduleName WEBTOOLS
%define exportName WEBTOOLS
%define cvstag V00-09-00 
%define cvsserver cvs://:pserver:anonymous@cmscvs.cern.ch:2401/cvs_server/repositories/CMSSW?passwd=AA_:yZZ3e
Source: %cvsserver&strategy=checkout&module=%{moduleName}&nocache=true&export=%{exportName}&tag=-r%{cvstag}&output=/%{moduleName}.tar.gz
Provides: perl(CGI) 
Provides: perl(Crypt::CBC) 
Provides: perl(SecurityModule) 

%prep
%setup -n %{moduleName}
%build
%install
mkdir -p %i/etc
cp -r * %i
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

%post
%{relocateConfig}etc/cherrypy.conf
%{relocateConfig}etc/apache2.conf
%{relocateConfig}etc/apache2-header.conf
%{relocateConfig}etc/apache2-footer.conf


