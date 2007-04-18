### RPM external yui 2.2.1
Requires: gcc-wrapper
%define realv %v
Source: http://switch.dl.sourceforge.net/sourceforge/yui/yui_%realv.zip 

%prep
rm -rf %{_builddir}/yui
mkdir -p %{_builddir}/yui
cd %{_builddir}
unzip %{_sourcedir}/yui_%realv.zip 
%build
## IMPORT gcc-wrapper
%install
pwd
cp -r yui/* %i
mkdir %i/etc
cat << \EOF_CHERRYPY_CONF > %i/etc/cherrypy.conf
# Serve a complete directory 
[/] 
tools.staticdir.on = True 
tools.staticdir.dir = %i/build
EOF_CHERRYPY_CONF
%post
%{relocateConfig}etc/cherrypy.conf
