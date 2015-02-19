### RPM cms PHEDEX-lifecycle 1.2.1
# Dummy line to force a rebuild
## INITENV +PATH PERL5LIB %i/perl_lib
## INITENV +PATH PERL5LIB %i/T0/perl_lib
%define downloadn %(echo %n | cut -f1 -d-)
%define downloadp %(echo %n | cut -f2 -d- | tr '[a-z]' '[A-Z]')
%define downloadt %(echo %realversion | tr '.' '_')
%define setupdir  %{downloadn}-%{downloadp}_%{downloadt}
Source: https://github.com/dmwm/PHEDEX/archive/%{downloadp}_%{downloadt}.tar.gz

#%define gittag 58f3eed1c98b8edaae10f6befe9d0343c0abc38b
#Source0: git://github.com/dmwm/PHEDEX?obj=PHEDEX-LifeCycle/%gittag&export=%n&output=/%n.tar.gz

# TODO Need to get this from somewhere else...
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

#Provides: perl(XML::LibXML)
Provides: perl(XML::Twig)
Provides: perl(T0::FileWatcher)
Provides: perl(T0::Logger::Sender)
Provides: perl(T0::Util)

# Actually, it is p5-xml-parser that requires this, but it doesn't configure itself correctly
# This is so it gets into our dependencies-setup.sh
#Requires:  expat

%prep
%setup -n %{setupdir}
tar zxf %_sourcedir/T0.tar.gz
rm Testbed/AutomatedTesting/check_API.pl

%build
%install
mkdir -p %i/etc/{env,profile}.d %i/bin
tar -cf - * | (cd %i && tar -xf -)
cp -p Testbed/LifeCycle/Lifecycle.pl %i/bin
cp -p Testbed/LifeCycle/CheckProxy.pl %i/bin
cp -p Testbed/LifeCycle/fake-delete.pl %i/bin
cp -p Testbed/LifeCycle/fake-validate.pl %i/bin
cp -p Testbed/FakeFTS.pl %i/bin

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
