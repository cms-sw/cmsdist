### RPM cms PHEDEX-admin PHEDEX_3_3_2

## INITENV +PATH PERL5LIB %i/perl_lib
%define downloadn %(echo %n | cut -f1 -d-)
Source: cvs://:pserver:anonymous@cmscvs.cern.ch:2401/cvs_server/repositories/CMSSW?passwd=AA_:yZZ3e&module=%{downloadn}&export=%{downloadn}&&tag=-r%{v}&output=/%{downloadn}.tar.gz
# Oracle libs
Requires: oracle oracle-env 
# perl libs
Requires: p5-time-hires p5-text-glob p5-compress-zlib p5-dbi
Requires: p5-dbd-oracle p5-xml-parser p5-poe p5-poe-component-child
Requires: p5-log-log4perl p5-log-dispatch p5-log-dispatch-filerotate
Requires: p5-params-validate p5-monalisa-apmon
# Actually, it is p5-xml-parser that requires this, but it doesn't configure itself correctly
# This is so it gets into our dependencies-setup.sh
Requires: expat

# Provided by system perl
Provides: perl(HTML::Entities)
Provides: perl(DB_File)
Provides: perl(Date::Manip)
Provides: perl(XML::LibXML)

%prep
%setup -n %{downloadn}
rm -rf Toolkit/DBS

%build

%install
mkdir -p %i/etc
tar -cf - * | (cd %i && tar -xf -)

# Set permissions
chmod 755 %i/Utilities/*

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
# bla bla
