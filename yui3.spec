### RPM external yui3 3.3.0
Source: http://yuilibrary.com/downloads/yui3/yui_%realversion.zip

%prep
rm -rf %{_builddir}/yui
mkdir -p %{_builddir}/yui
cd %{_builddir}
unzip %{_sourcedir}/yui_%realversion.zip 
%build
%install
pwd
cp -r yui/* %i
rm -rf %i/{examples,tests}
mkdir -p %i/etc
cat << \EOF_CHERRYPY_CONF > %i/etc/cherrypy.conf
# Serve a complete directory 
[/] 
tools.staticdir.on = True 
tools.staticdir.dir = %i/build
EOF_CHERRYPY_CONF
%post
%{relocateConfig}etc/cherrypy.conf
