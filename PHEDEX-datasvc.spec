### RPM cms PHEDEX-datasvc DATASVC_0_0_1
#
## INITENV +PATH PERL5LIB %i/perl_lib
%define downloadn %(echo %n | cut -f1 -d-)

Source: cvs://:pserver:anonymous@cmscvs.cern.ch:2401/cvs_server/repositories/CMSSW?passwd=AA_:yZZ3e&module=%{downloadn}&export=%{downloadn}&&tag=-r%{v}&output=/%{downloadn}.tar.gz
Requires: oracle oracle-env p5-time-hires p5-text-glob p5-compress-zlib p5-dbi p5-dbd-oracle p5-xml-parser
Requires: p5-monalisa-apmon p5-cgi p5-json-xs p5-apache-dbi
Requires: apache2-conf

# Actually, it is p5-xml-parser that requires this, but it doesn't configure itself correctly
# This is so it gets into our dependencies-setup.sh
Requires:  expat

# Provided by system perl
Provides: perl(HTML::Entities)
Provides: perl(DB_File)

%prep
%setup -n %{downloadn}

%build

%install
mkdir -p %i/etc
tar -cf - * | (cd %i && tar -xf -)

# Switch template variables in the configuration files

export DOCUMENT_ROOT=%i/PhEDExWeb/DataService
export CACHE_DIRECTORY=/tmp/phedex-datasvc
perl -p -i -e "s|\@DOCUMENT_ROOT\@|$DOCUMENT_ROOT|g;
	       s|\@CACHE_DIRECTORY\@|$CACHE_DIRECTORY|g;" %i/PhEDExWeb/DataService/conf/*

# Copy dependencies to dependencies-setup.sh
mkdir -p %i/etc/profile.d
for x in %pkgreqs; do
 case $x in /* ) continue ;; esac
 p=%{instroot}/%{cmsplatf}/$(echo $x | sed 's/\([^+]*\)+\(.*\)+\([A-Z0-9].*\)/\1 \2 \3/' | tr ' ' '/')
 echo ". $p/etc/profile.d/init.sh" >> %i/etc/profile.d/dependencies-setup.sh
 echo "source $p/etc/profile.d/init.csh" >> %i/etc/profile.d/dependencies-setup.csh
done

%post
mkdir -p /tmp/phedex-datasvc
%{relocateConfig}PhEDExWeb/DataService/conf/datasvc-app.conf
%{relocateConfig}PhEDExWeb/DataService/conf/datasvc-httpd.conf
%{relocateConfig}etc/profile.d/dependencies-setup.sh
%{relocateConfig}etc/profile.d/dependencies-setup.csh
