### RPM cms PHEDEX-lifecycle LIFECYCLE_1_0_0

## INITENV +PATH PERL5LIB %i/perl_lib
Source: cvs://:pserver:anonymous@cmscvs.cern.ch:2401/cvs_server/repositories/CMSSW?passwd=AA_:yZZ3e&module=%n&export=%n&&tag=-r%{v}&output=/%n.tar.gz

#Requires: oracle oracle-env
# perl libs
Requires: p5-time-hires p5-text-glob p5-compress-zlib p5-poe
Requires: p5-dbd-oracle p5-dbi p5-xml-parser p5-monalisa-apmon
Requires: p5-poe-component-child p5-log-log4perl p5-log-dispatch
Requires: p5-log-dispatch-filerotate p5-params-validate
# Actually, it is p5-xml-parser that requires this, but it doesn't configure itself correctly
# This is so it gets into our dependencies-setup.sh
Requires: expat

# Provided by system perl
#Provides: perl(HTML::Entities)
#Provides: perl(DB_File)
#Provides: perl(Date::Manip)
#Provides: perl(XML::LibXML)

%prep
%setup -n %n

%build

%install
mkdir -p %i/etc
tar -cf - * | (cd %i && tar -xf -)

# Set permissions
chmod 755 %i/Utilities/* Testbed/Lifecycle/*pl

# Copy dependencies to dependencies-setup.sh
mkdir -p %i/etc/profile.d
for x in %pkgreqs; do
 case $x in /* ) continue ;; esac
 p=%{instroot}/%{cmsplatf}/$(echo $x | sed 's/\([^+]*\)+\(.*\)+\([A-Z0-9].*\)/\1 \2 \3/' | tr ' ' '/')
 echo ". $p/etc/profile.d/init.sh" >> %i/etc/profile.d/dependencies-setup.sh
 echo "source $p/etc/profile.d/init.csh" >> %i/etc/profile.d/dependencies-setup.csh
done

# Make "env.sh" = "init.sh" for legacy configs
echo ". %i/etc/profile.d/init.sh" > %i/etc/profile.d/env.sh
echo "source %i/etc/profile.d/init.csh" > %i/etc/profile.d/env.csh

%post
%{relocateConfig}etc/profile.d/env.sh
%{relocateConfig}etc/profile.d/env.csh
%{relocateConfig}etc/profile.d/dependencies-setup.sh
%{relocateConfig}etc/profile.d/dependencies-setup.csh
