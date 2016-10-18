### RPM cms PHEDEX-lifecycle 1.3.0pre1
## INITENV +PATH PERL5LIB %i/perl_lib
## INITENV +PATH PERL5LIB %i/T0/perl_lib
%define downloadn %(echo %n | cut -f1 -d-)
%define downloadp %(echo %n | cut -f2 -d- | tr '[a-z]' '[A-Z]')
%define downloadt %(echo %realversion | tr '.' '_')
%define setupdir  %{downloadn}-%{downloadp}_%{downloadt}
Source: https://github.com/dmwm/PHEDEX/archive/%{downloadp}_%{downloadt}.tar.gz

# TODO Need to get this from somewhere else...
# TODO Check with Dirk if this is still needed (NR).
%define cvsserver cvs://:pserver:anonymous@cmssw.cvs.cern.ch:/local/reps/CMSSW?passwd=AA_:yZZ3e
Source1: %cvsserver&strategy=export&module=T0&export=T0&&tag=-rPHEDEX_LIFECYCLE_1_0_0&output=/T0.tar.gz

Requires: p5-poe p5-poe-component-child p5-clone p5-time-hires p5-text-glob
Requires: p5-compress-zlib p5-log-log4perl p5-json-xs p5-xml-parser p5-monalisa-apmon
Requires: p5-common-sense
Requires: mod_perl2 
Requires: lifecycle-dataprovider
# This is temporary, for the examples
Requires: dbs3-client
# The lifecycle doesn't require Oracle itself, but setting up a DB will!
Requires: oracle oracle-env p5-dbi p5-dbd-oracle
# add PHEDEX to fix perl dependency problem
Requires: PHEDEX

Provides: perl(XML::Twig)
Provides: perl(T0::FileWatcher)
Provides: perl(T0::Logger::Sender)
Provides: perl(T0::Util)

%prep
%setup -n %{setupdir}
tar zxf %_sourcedir/T0.tar.gz

%build
%install
mkdir -p %i/etc/{env,profile}.d
# Instead of taking all sources unpack only what belongs to the lifecycle:
# tar -cf - * | (cd %i && tar -xf -)

tar -c perl_lib/PHEDEX/{Core,Testbed} | tar -x -C %i 
tar -c Testbed/{Integration,LifeCycle} | tar -x -C %i
tar -c T0 | tar -x -C %i

# Generate dependencies-setup.{sh,csh} so init.{sh,csh} picks full environment.
: > %i/etc/profile.d/dependencies-setup.sh
: > %i/etc/profile.d/dependencies-setup.csh
#echo export LIFECYCLE=%instroot/Testbed/LifeCycle >> %i/etc/profile.d/dependencies-setup.sh
#echo setenv LIFECYCLE %instroot/Testbed/LifeCycle >> %i/etc/profile.d/dependencies-setup.csh
for tool in $(echo %{requiredtools} | sed -e's|\s+| |;s|^\s+||'); do
  root=$(echo $tool | tr a-z- A-Z_)_ROOT; eval r=\$$root
  if [ X"$r" != X ] && [ -r "$r/etc/profile.d/init.sh" ]; then
    echo "test X\$$root != X || . $r/etc/profile.d/init.sh" >> %i/etc/profile.d/dependencies-setup.sh
    echo "test X\$?$root = X1 || source $r/etc/profile.d/init.csh" >> %i/etc/profile.d/dependencies-setup.csh
  fi
done

%post
%{relocateConfig}etc/profile.d/dependencies-setup.*sh
