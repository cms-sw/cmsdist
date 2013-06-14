### RPM lcg SCRAM V0_20_1
## INITENV +PATH PATH %instroot/bin

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

%define cvsrepo cvs://:pserver:anonymous@spitools.cvs.cern.ch:2401/cvs/SPITOOLS?passwd=Ah<Z

Source0: %{cvsrepo}&tag=-r%{v}&module=%n&output=/source.tar.gz
Requires: p5-libwww-perl cms-env
Patch: scram-detect-make
Patch2: scram-no-check-env
Provides: perl(ActiveDoc::UserInterface_basic)
Provides: perl(ActiveDoc::UserQuery)
Provides: perl(ActiveDoc::GroupChecker)
Provides: perl(ObjectStore)
Provides: perl(Utilities::AddDir)
Provides: perl(Utilities::GroupChecker)
Provides: perl(Utilities::SCRAMUtils)

%prep
%setup -n %n
pwd
%patch -p1
%patch2 -p1
rm src/URL/test/test_URL_cvsfile.pm
%build
%install
tar -cf - . | tar -C %i -xvvf -

mkdir -p %instroot/bin %instroot/share/scramdbv0
mkdir -p %i/bin
touch %instroot/share/scramdbv0/project.lookup
[ -f %i/bin/scramv0 ] && rm %i/bin/scramv0
cat > %i/bin/scramv0 << \EOF
#!/bin/sh

# FIXME: Handle -re?
# FIXME: Since we can install the same package on many platforms in
# one tree, should the project lookup database be platform-specific?

SCRAM=$0
: ${SCRAM_HOME=%i}
: ${SCRAM_LOOKUPDB=%instroot/share/scramdbv0/project.lookup}
: ${SCRAMPERL="/usr/bin/env perl"}
PERL5LIB=$SCRAM_HOME/src${PERL5LIB+":$PERL5LIB"}
: ${SITENAME=CERN}
: ${SEARCHOVRD=true}
: ${LOCTOOLS=NODEFAULT}
export SCRAM SCRAM_HOME SCRAM_LOOKUPDB SCRAMPERL
export PERL5LIB SITENAME SEARCHOVRD LOCTOOLS

exec perl "$SCRAM_HOME/src/scramcli" ${1+"$@"}
EOF

[ -f %instroot/bin/scramv0 ] && rm %instroot/bin/scramv0
cat > %instroot/bin/scramv0 << \EOF_BIN_SCRAMV0
#!/bin/sh
source %instroot/`cmsarch`/lcg/%n/%v/etc/profile.d/init.sh
%instroot/`cmsarch`/lcg/%n/%v/bin/scramv0 $@
EOF_BIN_SCRAMV0

mkdir -p %{instroot}/%{cmsplatf}/etc/profile.d
mkdir -p %{i}/etc/profile.d
echo "#!/bin/sh" > %i/etc/profile.d/dependencies-setup.sh
echo "source $P5_LIBWWW_PERL_ROOT/etc/profile.d/init.sh" >> %i/etc/profile.d/dependencies-setup.sh
echo "#!/bin/csh" > %i/etc/profile.d/dependencies-setup.csh
echo "source $P5_LIBWWW_PERL_ROOT/etc/profile.d/init.csh" >> %i/etc/profile.d/dependencies-setup.csh

chmod 755 %instroot/bin/scramv0
chmod 755 %i/bin/scramv0
perl -p -i -e "s|#!.*perl|#!/usr/bin/env perl|" $(find %{i})
ln -sf scramv0 %{instroot}/bin/scram

%files
%i
%{instroot}/bin/scram
%{instroot}/bin/scramv0
%{instroot}/share/scramdbv0
%exclude %instroot/share/scramdbv0/project.lookup
%exclude %i/scripts/DrDOC.sh
%post
%{relocateConfig}etc/profile.d/dependencies-setup.sh
%{relocateConfig}etc/profile.d/dependencies-setup.csh
%{relocateConfig}bin/scramv0
perl -p -i -e "s|%instroot|$RPM_INSTALL_PREFIX|g" $RPM_INSTALL_PREFIX/bin/scramv0
