### RPM cms DMWMMON-datasvc 1.0.0
## INITENV +PATH PERL5LIB %i/perl_lib
%define downloadn %(echo %n | cut -f1 -d-)
%define downloadm PHEDEX
%define cvsversion DMWMMON_%(echo %realversion | tr . _)
%define cvsserver cvs://:pserver:anonymous@cmssw.cvs.cern.ch:/local/reps/CMSSW?passwd=AA_:yZZ3e
Source: %cvsserver&strategy=export&module=%{downloadm}&export=%{downloadn}&&tag=-r%{cvsversion}&output=/%{n}.tar.gz

# For DB Access
Requires: oracle oracle-env p5-dbi p5-dbd-oracle
# Core for web apps
Requires: apache-setup mod_perl2 p5-apache-dbi p5-cgi p5-cgi-session
# Useful for web apps
Requires: p5-json-xs p5-xml-parser
# Misc. Utilities
Requires: p5-params-validate p5-clone p5-time-hires p5-text-glob p5-compress-zlib p5-sort-key p5-mail-rfc822-address
Requires: p5-log-log4perl

# Actually, it is p5-xml-parser that requires this, but it doesn't configure itself correctly
# This is so it gets into our dependencies-setup.sh
Requires:  expat

# Provided by system perl
Provides: perl(HTML::Entities)
Provides: perl(DB_File)
Provides: perl(Date::Manip)
Provides: perl(XML::LibXML)
Provides: perl(URI::Escape)

%prep
%setup -n DMWMMON

%build
mv %_builddir/DMWMMON/PhEDExWeb/DataService/static/{phedex,dmwmmon}_pod.css

%install
mkdir -p %i/etc/{env,profile}.d
tar -cf - * | (cd %i && tar -xf -)

# Generate dependencies-setup.{sh,csh} so init.{sh,csh} picks full environment.
ln -sf ../profile.d/init.sh %i/etc/env.d/11-datasvc.sh
: > %i/etc/profile.d/dependencies-setup.sh
: > %i/etc/profile.d/dependencies-setup.csh
for tool in $(echo %{requiredtools} | sed -e's|\s+| |;s|^\s+||'); do
  root=$(echo $tool | tr a-z- A-Z_)_ROOT; eval r=\$$root
  if [ X"$r" != X ] && [ -r "$r/etc/profile.d/init.sh" ]; then
    echo "test X\$$root != X || . $r/etc/profile.d/init.sh" >> %i/etc/profile.d/dependencies-setup.sh
    echo "test X\$?$root = X1 || source $r/etc/profile.d/init.csh" >> %i/etc/profile.d/dependencies-setup.csh
  fi
done

%post
%{relocateConfig}etc/profile.d/dependencies-setup.*sh
