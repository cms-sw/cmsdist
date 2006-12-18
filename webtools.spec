### RPM cms webtools alpha
%define moduleName WEBTOOLS
%define exportName WEBTOOLS
%define cvstag HEAD
%define cvsserver cvs://:pserver:anonymous@cmscvs.cern.ch:2401/cvs_server/repositories/CMSSW?passwd=AA_:yZZ3e
Source: %cvsserver&strategy=checkout&module=%{moduleName}&nocache=true&export=%{exportName}&tag=-r%{cvstag}&output=/%{moduleName}.tar.gz

%prep
%setup -n %{moduleName}
%build
%install
mkdir -p %i/etc
cp -r * %i
cat << \EOF_CHERRYPY_CONF > %i/etc/cherrypy.conf
# Serve a complete directory 
[/Common] 
static_filter.on = True 
static_filter.dir = "%i/Common"
[/Templates]
static_filter.on = True
static_filter.dir = "%i/Templates"
EOF_CHERRYPY_CONF

%post
%{relocateConfig}etc/cherrypy.conf
