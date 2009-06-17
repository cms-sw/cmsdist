### RPM external yui 2.7.0
Source: http://switch.dl.sourceforge.net/sourceforge/yui/yui_%realversion.zip 

%prep
rm -rf %{_builddir}/yui
mkdir -p %{_builddir}/yui
cd %{_builddir}
unzip %{_sourcedir}/yui_%realversion.zip 
%build
%install
pwd
cp -r yui/* %i
mkdir -p %i/etc
cat << \EOF_CHERRYPY_CONF > %i/etc/cherrypy.conf
# Serve a complete directory 
[/] 
tools.staticdir.on = True 
tools.staticdir.dir = %i/build
EOF_CHERRYPY_CONF
%post
%{relocateConfig}etc/cherrypy.conf
