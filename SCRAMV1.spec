### RPM lcg SCRAM V1_0_2
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

%define cvsrepo  cvs://:pserver:anonymous@cmscvs.cern.ch:2401/cvs_server/repositories/SCRAM?passwd=AA_:yZZ3e 

Source0: %{cvsrepo}&tag=-r%{v}&module=%n&output=/source.tar.gz

%prep
%setup -n SCRAM

%build
%install
tar -cf - . | tar -C %i -xvvf -

mkdir -p %instroot/bin %instroot/share/scramdb
cat > %instroot/bin/scram << \EOF
#!/bin/sh

# FIXME: Handle -re?
# FIXME: Since we can install the same package on many platforms in
# one tree, should the project lookup database be platform-specific?

SCRAM=$0
: ${SCRAM_HOME=%i}
: ${SCRAM_LOOKUPDB=%instroot/share/scramdb/project.lookup}
: ${SCRAMPERL="/usr/bin/env perl"}
PERL5LIB=$SCRAM_HOME/src${PERL5LIB+":$PERL5LIB"}
: ${SITENAME=CERN}
: ${SEARCHOVRD=true}
: ${LOCTOOLS=NODEFAULT}
export SCRAM SCRAM_HOME SCRAM_LOOKUPDB SCRAMPERL
export PERL5LIB SITENAME SEARCHOVRD LOCTOOLS

exec perl "$SCRAM_HOME/src/scramcli" ${1+"$@"}
EOF
chmod 755 %instroot/bin/scram

%files
%i
%instroot/bin/scram
%instroot/share/scramdb
