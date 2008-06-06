### RPM lcg SCRAMV1 V1_2_1b
## INITENV +PATH PATH %instroot/common

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
# FIXME: should we have more than one project database and link them
# together into one big one?

%define cvsrepo  cvs://:pserver:anonymous@cmscvs.cern.ch:/cvs_server/repositories/CMSSW?passwd=AA_:yZZ3e
%define cvstag %v
Source0: %{cvsrepo}&tag=-r%{cvstag}&module=SCRAM&output=/source.tar.gz

%prep
#SCRAM version policy check
%define SCRAM_REL_SERIES %(echo %v | grep '^V[0-9]\\+_[0-9]\\+_[0-9]\\+' | sed 's|^\\(V[0-9]\\+_[0-9]\\+\\)_.*|\\1|')
if [ "X%{SCRAM_REL_SERIES}" == "X" ] ; then 
  echo "You are trying to build SCRAM version %v which does not follow the SCRAM version policy. Valid SCRAM versions should be of the form V[0-9]+_[0-9]+_[0-9].*"
  exit 1
fi
%setup -n SCRAM
%build
%install
tar -cf - . | tar -C %i -xvvf -

mkdir -p %i/src/main %instroot/%cmsplatf/lcg/SCRAMV1/scramdb
touch %instroot/%cmsplatf/lcg/SCRAMV1/scramdb/project.lookup

#SCRAM/INSTALL.txt recomendations
sed -i -e "s|@SCRAM_LOOKUPDB_DIR@|%instroot/%cmsplatf/lcg/SCRAMV1/scramdb/|g;s|@SCRAM_VERSION@|%v|g" %i/bin/scram
ln -s ../../bin/scram %i/src/main/scram.pl
chmod 755 %i/bin/scram

mkdir -p %{instroot}/%{cmsplatf}/etc/profile.d
mkdir -p %{i}/etc/profile.d

%post
%{relocateConfig}bin/scram

mkdir -p $RPM_INSTALL_PREFIX/%{cmsplatf}/etc/default-scram
# default version for SCRAM release series Vx_y_
VERSION_STR="%v"
if [ -f $RPM_INSTALL_PREFIX/%{cmsplatf}/etc/default-scram/%{SCRAM_REL_SERIES} ] ; then
  VERSION_STR="$VERSION_STR `cat $RPM_INSTALL_PREFIX/%{cmsplatf}/etc/default-scram/%{SCRAM_REL_SERIES}`"
fi
echo $VERSION_STR | tr ' ' '\n' | sort | tail -1 > $RPM_INSTALL_PREFIX/%{cmsplatf}/etc/default-scram/%{SCRAM_REL_SERIES}
# default version in common
VERSION_STR="%v"
if [ -f $RPM_INSTALL_PREFIX/%{cmsplatf}/etc/default-scramv1-version ] ; then
  VERSION_STR="$VERSION_STR `cat $RPM_INSTALL_PREFIX/%{cmsplatf}/etc/default-scramv1-version`"
fi
echo $VERSION_STR | tr ' ' '\n' | sort | tail -1 > $RPM_INSTALL_PREFIX/%{cmsplatf}/etc/default-scramv1-version

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
