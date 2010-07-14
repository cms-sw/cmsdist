### RPM external protovis 3.2
Source: http://protovis-js.googlecode.com/files/protovis-%realversion.zip 

%prep
rm -rf %{_builddir}/protovis
mkdir -p %{_builddir}/protovis
cd %{_builddir}
unzip %{_sourcedir}/protovis-%realversion.zip 
%build
%install
pwd
cp -r protovis-%realversion/protovis-*js %i
mkdir -p %i/etc
cat << \EOF_CHERRYPY_CONF > %i/etc/cherrypy.conf
# Serve a complete directory 
[/] 
tools.staticdir.on = True 
tools.staticdir.dir = %i/build
EOF_CHERRYPY_CONF
%post
%{relocateConfig}etc/cherrypy.conf
