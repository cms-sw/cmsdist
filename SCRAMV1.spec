### RPM lcg SCRAMV1 V1_1_0
## INITENV +PATH PATH %instroot/common
## INITENV +PATH PERL5LIB %{i}

%define perl /usr/bin/env perl
%if "%(echo %cmsplatf | cut -f1 -d_ | sed -e 's|\([A-Za-z]*\)[0-9]*|\1|')" == "osx"
%define perl /usr/bin/perl
%endif


Requires: p5-template-toolkit p5-uri p5-xml-parser p5-libwww-perl
Provides: perl(SCRAM::Helper)
Provides: perl(Utilities::AddDir) 
Provides: perl(Utilities::Architecture) 
Provides: perl(Utilities::SCRAMUtils)
Provides: perl(ActiveDoc::GroupChecker)
Provides: perl(ActiveDoc::UserInterface_basic)
Provides: perl(ActiveDoc::UserQuery)
Provides: perl(Doxygen::Context)
Provides: perl(Graph::Graph)
Provides: perl(ObjectStore)
Provides: perl(Utilities::SVNmodule)
Provides: perl(URL::URL_cvsfile)
Provides: perl(BuildSystem::Block)
Provides: perl(BuildSystem::Build)
Provides: perl(BuildSystem::BuildClass)
Provides: perl(BuildSystem::BuildSetup)
Provides: perl(BuildSystem::DateStampRecord)
Provides: perl(BuildSystem::Tool)
Provides: perl(BuildSystem::ToolBox)
Provides: perl(BuildSystem::ToolDoc)
Provides: perl(Utilities::GroupChecker) 

# This package is somewhat unusual compared to other packages we
# build: we install the normally versioned product "SCRAM", but also
# create the package database.  The latter do not follow the 
# standard versioning.
#
# The database is only created, but never changeed.  It is made part
# of this package, but none of the files in it are included, so if
# the package is removed, the directory will left intact.  (FIXME:
# check this is really so -- should we use %dir, or the default is
# good?)
#
# We do the install ourselves, as "Installation/install_scram" would
# do, but putting the results elsewhere and using our own scram
# wrapper instead of using the supplied one -- mainly for easier
# override of SCRAM_LOOKUPDB; the wrapper is really rather simple so
# there is no point in trying to patch it.
#
# FIXME: should we have more than one project database and link them
# together into one big one?

%define cvsrepo  cvs://:pserver:anonymous@cmscvs.cern.ch:/cvs_server/repositories/CMSSW?passwd=AA_:yZZ3e
%define cvstag V1_1_0_reltag
Source0: %{cvsrepo}&tag=-r%{cvstag}&module=SCRAM&output=/source.tar.gz

%prep
%setup -n SCRAM
%build
%install
tar -cf - . | tar -C %i -xvvf -
mkdir -p %instroot/%cmsplatf/lcg/SCRAMV1/scramdb %i/bin %i/Installation
touch %instroot/%cmsplatf/lcg/SCRAMV1/scramdb/project.lookup

cat Installation/scram.pl.in | sed -e "s|@PERLEXE@|%perl|;s|@SCRAM_HOME@|%i|g;s|@INSTALLDIR@|%i/src|g" > %i/bin/scram
cat Installation/scram.pl.in | sed -e "s|@PERLEXE@|%perl|;s|@SCRAM_HOME@|%i|g;s|@INSTALLDIR@|%i/src|g" > %i/src/main/scram.pl
chmod +x %i/src/main/scram.pl
cat Installation/SCRAM_SITE.pm.in | sed -e "s|@SCRAM_HOME@|%i|g;s|@SCRAM_LOOKUPDB_DIR@|%instroot/%cmsplatf/lcg/SCRAMV1/scramdb/|g;s|@PERLEXE@|%perl|;s|@TT2INSTALLDIR@|$TEMPLATE_TOOLKIT_ROOT/lib|g;s|@SITETEMPLATEDIR@|%i/Templates|g;s|@SCRAM_SITENAME@|STANDALONE|g" > %i/Installation/SCRAM_SITE.pm
sed -e "s|@SCRAM_VERSION@|%v|" src/SCRAM/SCRAM.pm > %i/src/SCRAM/SCRAM.pm
chmod 755 %i/bin/scram

mkdir -p %i/etc
echo $PERL5LIB > %i/etc/perl5lib.env

mkdir -p %{instroot}/%{cmsplatf}/etc/profile.d
mkdir -p %{i}/etc/profile.d
echo "#!/bin/sh" > %i/etc/profile.d/dependencies-setup.sh
echo "source $P5_TEMPLATE_TOOLKIT_ROOT/etc/profile.d/init.sh" >> %i/etc/profile.d/dependencies-setup.sh
echo "source $P5_URI_ROOT/etc/profile.d/init.sh" >> %i/etc/profile.d/dependencies-setup.sh
echo "source $P5_XML_PARSER_ROOT/etc/profile.d/init.sh" >> %i/etc/profile.d/dependencies-setup.sh
echo "source $P5_LIBWWW_PERL_ROOT/etc/profile.d/init.sh" >> %i/etc/profile.d/dependencies-setup.sh

echo "#!/bin/csh" > %i/etc/profile.d/dependencies-setup.csh
echo "source $P5_TEMPLATE_TOOLKIT_ROOT/etc/profile.d/init.csh" >> %i/etc/profile.d/dependencies-setup.csh
echo "source $P5_URI_ROOT/etc/profile.d/init.csh" >> %i/etc/profile.d/dependencies-setup.csh
echo "source $P5_XML_PARSER_ROOT/etc/profile.d/init.csh" >> %i/etc/profile.d/dependencies-setup.csh
echo "source $P5_LIBWWW_PERL_ROOT/etc/profile.d/init.csh" >> %i/etc/profile.d/dependencies-setup.csh

%perl -p -i -e "s|#!.*perl|#!%perl|" %{i}/doc/doxygen/DoxyFilt.pl

%post
%{relocateConfig}etc/perl5lib.env
%{relocateConfig}Installation/SCRAM_SITE.pm
%{relocateConfig}bin/scram
%{relocateConfig}src/main/scram.pl
%{relocateConfig}etc/profile.d/dependencies-setup.sh
%{relocateConfig}etc/profile.d/dependencies-setup.csh
# If and only if there is no default-scramv1 set the default to be the version we package in this spec.
OLD_VERSION=""
if [ -f $RPM_INSTALL_PREFIX/%{cmsplatf}/etc/default-scramv1-version ]
then
    mkdir -p $RPM_INSTALL_PREFIX/%{cmsplatf}/etc
    OLD_VERSION=`cat $RPM_INSTALL_PREFIX/%{cmsplatf}/etc/default-scramv1-version`
fi
NEW_VERSION=%v
(echo $OLD_VERSION;echo $NEW_VERSION) | sort | tail -1 > $RPM_INSTALL_PREFIX/%{cmsplatf}/etc/default-scramv1-version

mkdir -p $RPM_INSTALL_PREFIX/%cmsplatf/lcg/SCRAMV1/scramdb
touch $RPM_INSTALL_PREFIX/%cmsplatf/lcg/SCRAMV1/scramdb/project.lookup
if [ -f $RPM_INSTALL_PREFIX/share/scramdb/project.lookup ] ; then
  dblinked=`grep "DB $RPM_INSTALL_PREFIX/share/scramdb/project.lookup" $RPM_INSTALL_PREFIX/%cmsplatf/lcg/SCRAMV1/scramdb/project.lookup`
  if [ "X$dblinked" = "X" ] ; then
    echo '!DB' $RPM_INSTALL_PREFIX/share/scramdb/project.lookup > $RPM_INSTALL_PREFIX/%cmsplatf/lcg/SCRAMV1/scramdb/project.lookup.link
    cat $RPM_INSTALL_PREFIX/%cmsplatf/lcg/SCRAMV1/scramdb/project.lookup >> $RPM_INSTALL_PREFIX/%cmsplatf/lcg/SCRAMV1/scramdb/project.lookup.link
    mv $RPM_INSTALL_PREFIX/%cmsplatf/lcg/SCRAMV1/scramdb/project.lookup.link $RPM_INSTALL_PREFIX/%cmsplatf/lcg/SCRAMV1/scramdb/project.lookup
  fi
fi

%files
%i
%instroot/%cmsplatf/lcg/SCRAMV1/scramdb
%exclude %instroot/%cmsplatf/lcg/SCRAMV1/scramdb/project.lookup
%exclude %i/scripts/DrDOC.sh
