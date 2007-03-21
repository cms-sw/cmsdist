### RPM external yui 2.2.0a
Source: http://switch.dl.sourceforge.net/sourceforge/yui/yui_%v.zip 

%prep
rm -rf %{_builddir}/yui
mkdir -p %{_builddir}/yui
cd %{_builddir}
unzip %{_sourcedir}/yui_%v.zip 
%build
%install
pwd
cp -r yui/* %i
mkdir %i/etc
cat << \EOF_CHERRYPY_CONF > %i/etc/cherrypy.conf
# Serve a complete directory 
[/] 
static_filter.on = True 
static_filter.dir = %i/build
EOF_CHERRYPY_CONF
%post
%{relocateConfig}etc/cherrypy.conf
