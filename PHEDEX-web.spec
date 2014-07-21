### RPM cms PHEDEX-web 4.2.10
## INITENV +PATH PERL5LIB %i/perl_lib

%define downloadn %(echo %n | cut -f1 -d-)
%define downloadp %(echo %n | cut -f2 -d- | tr '[a-z]' '[A-Z]')
%define downloadt %(echo %realversion | tr '.' '_')
%define setupdir  %{downloadn}-%{downloadp}_%{downloadt}
Source: https://github.com/dmwm/PHEDEX/archive/%{downloadp}_%{downloadt}.tar.gz

#%define gittag 1cf6be60c2447feb33c8394e047b2b8a1285983a
#Source: git://github.com/dmwm/PHEDEX?obj=PHEDEX-web/%gittag&export=%n&output=/%n.tar.gz

# This allows me to not pull everything in here, which duplicates code
Requires: PHEDEX-datasvc

# For DB Access
Requires: oracle oracle-env p5-dbi p5-dbd-oracle
# Core for web apps
Requires: apache-setup mod_perl2 p5-apache-dbi webtools p5-cgi p5-cgi-session
# Useful for web apps
Requires: p5-json-xs p5-xml-parser
# Misc. Utilities
Requires: p5-params-validate p5-clone p5-time-hires p5-text-glob p5-compress-zlib p5-sort-key p5-mail-rfc822-address
Requires: p5-log-log4perl
# For GraphTool component
Requires: py2-pil py2-matplotlib py2-numpy libjpg py2-pytz

# Actually, it is p5-xml-parser that requires this, but it doesn't configure itself correctly
# This is so it gets into our dependencies-setup.sh
Requires:  expat

# Provided by system perl
Provides: perl(HTML::Entities)
Provides: perl(DB_File)
Provides: perl(XML::LibXML)

%prep
%setup -n %{setupdir}
rm -rf Build Custom Testbed Utilities
rm -rf Contrib Deployment Migration PhEDExWeb Schema Toolkit VERSION
rm -rf Documentation/{ACAT2008,ChangeLog,cpan_min.css,DC04PostMortem,DC04Stats,Grid2005,MakePerlDocs.pl,Updates,WhitePapers}
rm -rf perl_lib/{DMWMMON,template}
rm -rf perl_lib/PHEDEX/{BlockActivate,BlockDelete,Debug.pm,Monalisa.pm,Testbed,BlockAllocator,BlockLatency,Error,Monitoring,Transfer,BlockArrive,BlockMonitor,File,Namespace,BlockConsistency,CLI,Infrastructure,BlockDeactivate,LoadTest,Schema}
rm perl_lib/PHEDEX/RequestAllocator/Agent.pm
rm -rf perl_lib/PHEDEX/Core/{Agent,Config.pm,Net.pm,Agent.pm,JobManager.pm,phedex_logger.conf,RFIO.pm,Command.pm,Help.pm,Logging.pm,SQLPLUS.pm,Config}
rm -rf perl_lib/PHEDEX/Web/SQLSpace.pm
rm -rf perl_lib/PHEDEX/Web/API/{Mongo.pm,RequestSetStateFake.pm,StorageInsert.pm,StorageUsage.pm}

%build
%install
mkdir -p %i/etc/{env,profile}.d

tar -cf - * | (cd %i && tar -xf -)
rm -r %i/Documentation/WebConfig %i/Documentation/WebSite/PlotConfig/config

# Overwrite graph server daemon; only temporarily here until included in CVS.
cat > %i/Documentation/WebSite/PlotConfig/tools/phedex-web.py <<-EOF 
	#!/usr/bin/env python
	from graphtool.base.xml_config import XmlConfig
	import sys, cherrypy
	xc = XmlConfig(file=sys.argv[1]) 
	cherrypy.server.quickstart()
	cherrypy.engine.start() 
	xc.globals['web'].kill()
EOF

python -m compileall %i || true

# Generate dependencies-setup.{sh,csh} so init.{sh,csh} picks full environment.
ln -sf ../profile.d/init.sh %i/etc/env.d/10-web.sh
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
