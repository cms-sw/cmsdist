### RPM cms PHEDEX-web WEB_3_0_2
#
## INITENV +PATH PERL5LIB %i/perl_lib
%define downloadn %(echo %n | cut -f1 -d-)
%define nversion %(echo %v | sed 's|WEB_||' | sed 's|_|.|g')
%define cvsserver cvs://:pserver:anonymous@cmscvs.cern.ch:2401/cvs_server/repositories/CMSSW?passwd=AA_:yZZ3e

Source: %cvsserver&strategy=checkout&module=%{downloadn}&export=%{downloadn}&&tag=-r%{v}&output=/%{downloadn}.tar.gz
Requires: oracle oracle-env p5-time-hires p5-text-glob p5-compress-zlib p5-dbi p5-dbd-oracle p5-xml-parser
Requires: p5-monalisa-apmon p5-poe p5-cgi p5-cgi-session p5-json-xs p5-apache-dbi p5-sort-key
Requires: py2-pil py2-matplotlib py2-numpy libjpg
Requires: apache2-conf webtools dbs-client

# Actually, it is p5-xml-parser that requires this, but it doesn't configure itself correctly
# This is so it gets into our dependencies-setup.sh
Requires:  expat

# Provided by system perl
Provides: perl(HTML::Entities)
Provides: perl(DB_File)
Provides: perl(XML::LibXML)

%prep
%setup -n %{downloadn}

%build

%install
mkdir -p %i/etc
tar -cf - * | (cd %i && tar -xf -)

# Switch template variables in the configuration files
export PHEDEX_ROOT=%i
export APACHE2_CONFIG_ROOT=$APACHE2_CONFIG_ROOT
perl -p -i -e "s|\@PHEDEX_ROOT\@|$PHEDEX_ROOT|g;
	       s|\@APACHE2_CONF_ROOT\@|$APACHE2_CONF_ROOT|g" %i/Documentation/WebConfig/* %i/Documentation/WebSite/PlotConfig/config/*

# Copy dependencies to dependencies-setup.sh
mkdir -p %i/etc/profile.d
for x in %pkgreqs; do
 case $x in /* ) continue ;; esac
 p=%{instroot}/%{cmsplatf}/$(echo $x | sed 's/\([^+]*\)+\(.*\)+\([A-Z0-9].*\)/\1 \2 \3/' | tr ' ' '/')
 echo ". $p/etc/profile.d/init.sh" >> %i/etc/profile.d/dependencies-setup.sh
 echo "source $p/etc/profile.d/init.csh" >> %i/etc/profile.d/dependencies-setup.csh
done

# cp startup scripts to /bin
mkdir -p %i/bin
cp %i/Documentation/WebConfig/cmsweb_phedex* %i/bin

%post
%{relocateConfig}Documentation/WebConfig/phedexweb-httpd.conf
%{relocateConfig}Documentation/WebConfig/phedexweb-app.conf
%{relocateConfig}Documentation/WebConfig/phedexweb-secmod.conf
%{relocateConfig}Documentation/WebSite/PlotConfig/config/cherrypy_prod.conf
%{relocateConfig}bin/cmsweb_phedex
%{relocateConfig}bin/cmsweb_phedex_graphs
%{relocateConfig}etc/profile.d/dependencies-setup.sh
%{relocateConfig}etc/profile.d/dependencies-setup.csh
