### RPM lcg SCRAMV1 V1_0_2
## INITENV +PATH PATH %instroot/bin
## INITENV +PATH PERL5LIB %{i}
Requires: expat p5-template-toolkit p5-uri p5-xml-parser p5-libwww-perl cms-env
Requires: scramv1-wrapper
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

# This package is somewhat unusual compared to other packages we
# build: we install the normally versioned product "SCRAM", but also
# create the front-end "scram" wrapper and the package database.  The
# latter do not follow the standard versioning.
#
# The front-end script can be overwritten by any version *PROVIDED*
# the platform string comes first as is the default (i.e. the
# installation tree looks like <platf>/lcg/SCRAM/<version>/src).
#
# The database is only created, but never changeed.  It is made part
# of this package, but none of the files in it are included, so if
# the package is removed, the directory will left intact.  (FIXME:
# check this is really so -- should we use %dir, or the default is
# good?)
#
# The front-end wrapper and the script go at the installation root,
# not anywhere in the package tree.  They must remain modifiable.
#
# We do the install ourselves, as "Installation/install_scram" would
# do, but putting the results elsewhere and using our own scram
# wrapper instead of using the supplied one -- mainly for easier
# override of SCRAM_LOOKUPDB; the wrapper is really rather simple so
# there is no point in trying to patch it.
#
# FIXME: should we have more than one project database and link them
# together into one big one?

%define cvsrepo  cvs://:pserver:anonymous@cmscvs.cern.ch:2401/cvs_server/repositories/SCRAM?passwd=AA_:yZZ3e  

Source0: %{cvsrepo}&tag=-r%{v}&module=SCRAM&output=/source.tar.gz

%prep
%setup -n SCRAM
%build
%install
tar -cf - . | tar -C %i -xvvf -
rm -rf %i/cgi
mkdir -p %instroot/bin %instroot/share/scramdb %i/Installation
mkdir -p %i/bin
touch %instroot/share/scramdb/project.lookup

cat Installation/scram.pl.in | sed -e "s|@PERLEXE@|/usr/bin/env perl|;s|@SCRAM_HOME@|%i|;s|@INSTALLDIR@|%i/src|" > %i/bin/scramv1
cat Installation/scram.pl.in | sed -e "s|@PERLEXE@|/usr/bin/env perl|;s|@SCRAM_HOME@|%i|;s|@INSTALLDIR@|%i/src|" > %i/src/main/scram.pl
chmod +x %i/src/main/scram.pl
cat Installation/SCRAM_SITE.pm.in | sed -e "s|@SCRAM_HOME@|%i|;s|@SCRAM_LOOKUPDB_DIR@|%instroot/share/scramdb/|;s|@PERLEXE@|/usr/bin/env perl|;s|@TT2INSTALLDIR@|$TEMPLATE_TOOLKIT_ROOT/lib|;s|@SITETEMPLATEDIR@|%i/Templates|;s|@SCRAM_SITENAME@|STANDALONE|" > %i/Installation/SCRAM_SITE.pm

# cat > %instroot/bin/scramv1 << \EOF
# #!/bin/sh
# 
# # FIXME: Handle -re?
# # FIXME: Since we can install the same package on many platforms in
# # one tree, should the project lookup database be platform-specific?
# 
# SCRAM=$0
# : ${SCRAM_HOME=%i}
# : ${SCRAM_LOOKUPDB=%instroot/share/scramdb/project.lookup}
# : ${SCRAMPERL="/usr/bin/env perl"}
# PERL5LIB=$SCRAM_HOME/src${PERL5LIB+":$PERL5LIB"}
# : ${SITENAME=CERN}
# : ${SEARCHOVRD=true}
# : ${LOCTOOLS=NODEFAULT}
# export SCRAM SCRAM_HOME SCRAM_LOOKUPDB SCRAMPERL
# export PERL5LIB SITENAME SEARCHOVRD LOCTOOLS
# 
# exec perl "$SCRAM_HOME/src/scramcli" ${1+"$@"}
# EOF
chmod 755 %i/bin/scramv1

mkdir %i/etc
echo $PERL5LIB > %i/etc/perl5lib.env

mkdir -p %{instroot}/%{cmsplatf}/etc/profile.d
mkdir -p %{i}/etc/profile.d
echo "#!/bin/sh" > %i/etc/profile.d/dependencies-setup.sh
echo "source $EXPAT_ROOT/etc/profile.d/init.sh" >> %i/etc/profile.d/dependencies-setup.sh
echo "source $P5_TEMPLATE_TOOLKIT_ROOT/etc/profile.d/init.sh" >> %i/etc/profile.d/dependencies-setup.sh
echo "source $P5_URI_ROOT/etc/profile.d/init.sh" >> %i/etc/profile.d/dependencies-setup.sh
echo "source $P5_XML_PARSER_ROOT/etc/profile.d/init.sh" >> %i/etc/profile.d/dependencies-setup.sh
echo "source $P5_LIBWWW_PERL_ROOT/etc/profile.d/init.sh" >> %i/etc/profile.d/dependencies-setup.sh

echo "#!/bin/csh" > %i/etc/profile.d/dependencies-setup.csh
echo "source $EXPAT_ROOT/etc/profile.d/init.csh" >> %i/etc/profile.d/dependencies-setup.csh
echo "source $P5_TEMPLATE_TOOLKIT_ROOT/etc/profile.d/init.csh" >> %i/etc/profile.d/dependencies-setup.csh
echo "source $P5_URI_ROOT/etc/profile.d/init.csh" >> %i/etc/profile.d/dependencies-setup.csh
echo "source $P5_XML_PARSER_ROOT/etc/profile.d/init.csh" >> %i/etc/profile.d/dependencies-setup.csh
echo "source $P5_LIBWWW_PERL_ROOT/etc/profile.d/init.csh" >> %i/etc/profile.d/dependencies-setup.csh

perl -p -i -e "s|#!.*perl|/usr/bin/env perl|" %{i}/doc/doxygen/DoxyFilt.pl

%post
%{relocateConfig}etc/perl5lib.env
%{relocateConfig}Installation/SCRAM_SITE.pm
%{relocateConfig}bin/scramv1
%{relocateConfig}src/main/scram.pl
%{relocateConfig}etc/profile.d/dependencies-setup.sh
%{relocateConfig}etc/profile.d/dependencies-setup.csh
# If and only if there is no default-scramv1 set the default to be the version we package in this spec.
mkdir -p $RPM_INSTALL_PREFIX/%{cmsplatf}/etc
OLD_VERSION=""
if [ ! -f $RPM_INSTALL_PREFIX/%{cmsplatf}/etc/default-scramv1-version ]
then
    OLD_VERSION=`cat $RPM_INSTALL_PREFIX/%{cmsplatf}/etc/default-scramv1-version`
fi
NEW_VERSION=%v
(echo $OLD_VERSION;echo $NEW_VERSION) | sort | tail -1 > $RPM_INSTALL_PREFIX/%{cmsplatf}/etc/default-scramv1-version

%files
%i
%instroot/share/scramdb
%exclude %instroot/share/scramdb/project.lookup
%exclude %i/scripts/DrDOC.sh
