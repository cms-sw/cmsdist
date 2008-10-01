### RPM cms apache2-conf 1.12c
# Configuration for additional apache2 modules
%define cvsserver cvs://:pserver:anonymous@cmscvs.cern.ch:2401/cvs_server/repositories/CMSSW?passwd=AA_:yZZ3e&strategy=export&nocache=true
Source0: %cvsserver&module=COMP/WEBTOOLS/Configuration&export=conf&tag=-rSERVER_CONF_1_12&output=/config.tar.gz
Requires: apache2
Obsoletes: cms+apache2-conf+1.10-cmp
Obsoletes: cms+apache2-conf+1.11-cmp
Obsoletes: cms+apache2-conf+1.9b-cmp
Obsoletes: cms+apache2-conf+1.9-cmp
Obsoletes: cms+apache2-conf+1.8-cmp
Obsoletes: cms+apache2-conf+1.7b-cmp
Obsoletes: cms+apache2-conf+1.7-cmp
Obsoletes: cms+apache2-conf+1.6-cmp
Obsoletes: cms+apache2-conf+1.5-cmp
Obsoletes: cms+apache2-conf+1.4-cmp
Obsoletes: cms+apache2-conf+1.3-cmp
Obsoletes: cms+apache2-conf+1.2-cmp
Obsoletes: cms+apache2-conf+1.1-cmp
Obsoletes: cms+apache2-conf+1.0-cmp

%prep
%setup -T -b 0 -n conf

%build

%install
# Make directory for various resources of this package.
rm -fr %instroot/apache2/*/*core-server*
mkdir -p %i/bin %i/htdocs %i/tools
mkdir -p %instroot/apache2/apps.d
mkdir -p %instroot/apache2/rewrites.d
mkdir -p %instroot/apache2/ssl_rewrites.d
mkdir -p %instroot/apache2/startenv.d
mkdir -p %instroot/apache2/htdocs
mkdir -p %instroot/apache2/conf/core-server
mkdir -p %instroot/apache2/logs
mkdir -p %instroot/apache2/var

# Make a server start script, with our environment.
sed 's/^  //' << EOF > %i/bin/httpd
  #!/bin/sh
  for file in %instroot/apache2/startenv.d/*.sh; do
    [ -f \$file ] || continue
    . \$file
  done
  exec $APACHE2_ROOT/bin/httpd -f %instroot/apache2/conf/core-server/apache2.conf \${1+"\$@"}
EOF
chmod +x %i/bin/httpd

# Replace template variables in configuration files with actual paths.
perl -p -i -e "s|\@SERVER_ROOT\@|%instroot|g;s|\@APACHE2_ROOT\@|$APACHE2_ROOT|g;" %_builddir/conf/apache2.conf

# Generate dependencies-setup.{sh,csh}.
rm -rf %i/etc/profile.d
mkdir -p %i/etc/profile.d
: > %i/etc/profile.d/dependencies-setup.sh
: > %i/etc/profile.d/dependencies-setup.csh
for tool in `echo %{requiredtools} | sed -e's|\s+| |;s|^\s+||'`; do
  eval toolroot=\$$(echo $tool | tr a-z- A-Z_)_ROOT
  if [ X"${toolroot:+set}" = Xset ] && [ -d "$toolroot" ]; then
    echo ". $toolroot/etc/profile.d/init.sh" >> %i/etc/profile.d/dependencies-setup.sh
    echo "source $toolroot/etc/profile.d/init.csh" >> %i/etc/profile.d/dependencies-setup.csh
  fi
done

# Copy files to the server setup directory.
cp -p %_builddir/conf/* %instroot/apache2/conf/core-server/
cp -p %i/etc/profile.d/dependencies-setup.sh %instroot/apache2/startenv.d/00-core-server.sh

%post
# Relocate files.
CFG=$RPM_INSTALL_PREFIX/apache2/conf/core-server
perl -p -i -e "s|%instroot|$RPM_INSTALL_PREFIX|g"	\
  $RPM_INSTALL_PREFIX/%pkgrel/bin/httpd			\
  $RPM_INSTALL_PREFIX/%pkgrel/etc/profile.d/*-*.*sh	\
  $RPM_INSTALL_PREFIX/apache2/conf/core-server/*.conf	\
  $RPM_INSTALL_PREFIX/apache2/startenv.d/00-core-server.sh

# Set ServerName.
T=$(mktemp) U=$(mktemp) H=$(hostname -f)
host cmsweb.cern.ch 2>/dev/null | grep 'has address' | awk '{print $NF}' > $T
host $H 2>/dev/null | grep 'has address' | awk '{print $NF}' > $U
[ $(fgrep -f $U < $T | wc -l) != 0 ] && H=cmsweb.cern.ch
rm -f $T $U

echo "Adjusting ServerName to $H."
perl -p -i -e 's/^ServerName (\S+)$/ServerName '$H'/g' $CFG/apache2.conf

# Build certificate bundles.
if [ -d /etc/grid-security/certificates ]; then
  echo "Building certificate bundles."
  for f in /etc/grid-security/certificates/*.info; do
    if grep "# CA CERN-" < $f > /dev/null; then
      cat $(dirname $f)/$(basename $f .info).0
      openssl crl -in $(dirname $f)/$(basename $f .info).r0
    fi
  done > $CFG/cern-ca.pem

  cat /etc/grid-security/certificates/*.0 > $CFG/grid-ca.pem
  echo /etc/grid-security/certificates/*.r0 | xargs -n1 openssl crl -in > $CFG/grid-crl.pem
else
  echo "No /etc/grid-security/certificates, please build certificate bundles yourself:"
  echo "   $CFG/cern-ca.pem"
  echo "   $CFG/grid-ca.pem"
  echo "   $CFG/grid-crl.pem"
fi

# Deter attempts to modify installed files locally.
find $RPM_INSTALL_PREFIX/apache2/*/*core-server* -type f |
  fgrep -v .pem | xargs chmod a-w

%files
%i/
%dir %instroot/apache2
%dir %instroot/apache2/var
%dir %instroot/apache2/logs
%dir %instroot/apache2/conf
%dir %instroot/apache2/htdocs
%dir %instroot/apache2/apps.d
%dir %instroot/apache2/startenv.d
%attr(444,-,-) %config %instroot/apache2/conf/core-server/*.conf
%attr(555,-,-) %config %instroot/apache2/conf/core-server/testme
#%config(missingok) %instroot/apache2/conf/core-server/cern-ca.pem
#%config(missingok) %instroot/apache2/conf/core-server/grid-ca.pem
#%config(missingok) %instroot/apache2/conf/core-server/grid-crl.pem
%attr(444,-,-) %config %instroot/apache2/startenv.d/00-core-server.sh
