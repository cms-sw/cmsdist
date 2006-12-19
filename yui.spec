### RPM external yui 0.12.1
Source: http://switch.dl.sourceforge.net/sourceforge/yui/yui_%v.zip 

%prep
%setup -n yui
%build
%install
cp -r * %i
mkdir %i/etc
cat << \EOF_CHERRYPY_CONF > %i/etc/cherrypy.conf
# Serve a complete directory 
[/] 
static_filter.on = True 
static_filter.dir = %i/build
EOF_CHERRYPY_CONF
%post
%{relocateConfig}etc/cherrypy.conf
