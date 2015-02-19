### RPM cms das-client 2.9.0
## INITENV +PATH PYTHONPATH %i/${PYTHON_LIB_SITE_PACKAGES}
%define pkg DAS
Source0: git://github.com/dmwm/DAS?obj=master/%realversion&export=%pkg&output=/%pkg.tar.gz
Requires: python

# RPM macros documentation
# http://www.rpm.org/max-rpm/s1-rpm-inside-macros.html
%prep
%setup -c
%setup -T -D -a 0

%build

%install
cd DAS
mkdir -p %i/{bin,etc}
cp src/python/DAS/tools/das_client.py %i/bin

# create wrapper script
cat > %i/bin/das-client << EOF
#!/bin/sh
case $(cmsos) in
    slc6_*) os=slc6 ;;
    slc5_*) os=slc5 ;;
    *) os=slc6 ;;
esac

# Sourcing dasclient environment
das_client=/cvmfs/cms.cern.ch/das/das_\$os.sh
if [ -f \$das_client ]
then
    source \$das_client;
elif [ -f /cvmfs/cms.cern.ch/das/das.sh ]
then
    source /cvmfs/cms.cern.ch/das/das.sh;
else
    echo "ERROR: DAS client not found in CVMFS '/cvmfs/cms.cern.ch'"
    exit 1
fi

if [ \$# == 0 ]
then
    \$DAS_CLIENT_ROOT/bin/das_client.py --help | sed 's/das_client.py/das_client/'
else
    \$DAS_CLIENT_ROOT/bin/das_client.py "\$@"
fi
EOF
chmod +x %i/bin/das-client

# create web area
mkdir -p %cmsroot/WEB/das-client
cp -r %i/bin/* %cmsroot/WEB/das-client/

# Generate dependencies-setup.{sh,csh} so init.{sh,csh} picks full environment.
mkdir -p %i/etc/profile.d
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

%files
%{installroot}/%{pkgrel}/
