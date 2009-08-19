### RPM cms apache2-conf 2.4
# Configuration for additional apache2 modules
%define cvsserver cvs://:pserver:anonymous@cmscvs.cern.ch:2401/cvs_server/repositories/CMSSW?passwd=AA_:yZZ3e&strategy=export&nocache=true
#Source0: %cvsserver&module=COMP/WEBTOOLS/Configuration&export=conf&tag=-rSERVER_CONF_2_4&output=/config.tar.gz
Source0: %cvsserver&module=COMP/WEBTOOLS/Configuration&export=conf&tag=-rHEAD&output=/config.tar.gz
Requires: apache2
Obsoletes: cms+apache2-conf+2.3-cmp
Obsoletes: cms+apache2-conf+2.2k-cmp
Obsoletes: cms+apache2-conf+2.2j-cmp
Obsoletes: cms+apache2-conf+2.2i-cmp
Obsoletes: cms+apache2-conf+2.2h-cmp
Obsoletes: cms+apache2-conf+2.2g-cmp
Obsoletes: cms+apache2-conf+2.2f-cmp
Obsoletes: cms+apache2-conf+2.2e-cmp
Obsoletes: cms+apache2-conf+2.2d-cmp
Obsoletes: cms+apache2-conf+2.2c-cmp
Obsoletes: cms+apache2-conf+2.2b-cmp
Obsoletes: cms+apache2-conf+2.2-cmp

%prep
%setup -T -b 0 -n conf

%build

%install
# Make directory for various resources of this package.
rm -f %instroot/apache2/etc/startenv.d/00-core-server.sh
rm -f %instroot/apache2/etc/init.d/httpd
rm -f %instroot/apache2/etc/archive-log-files
rm -f %instroot/apache2/conf/apache2.conf
rm -f %instroot/apache2/logs/start_stop.log

mkdir -p %i/bin
mkdir -p %instroot/apache2/apps.d
mkdir -p %instroot/apache2/htdocs
mkdir -p %instroot/apache2/conf
mkdir -p %instroot/apache2/logs
mkdir -p %instroot/apache2/var
mkdir -p %instroot/apache2/etc/init.d
mkdir -p %instroot/apache2/etc/startenv.d

# Replace template variables in configuration files with actual paths.
perl -p -i -e "s|\@SERVER_ROOT\@|%instroot/apache2|g;s|\@APACHE2_ROOT\@|$APACHE2_ROOT|g;" %_builddir/conf/apache2.conf

# Generate dependencies-setup.{sh,csh}.
rm -fr %i/etc/profile.d
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

# Replace template variables in the server startup script.
perl -p -i -e "s|\@SERVER_ROOT\@|%instroot/apache2|g;s|\@APACHE2_ROOT\@|$APACHE2_ROOT|g;" %_builddir/conf/httpd

# Create server options file.
echo "-DPRODUCTION" > %instroot/apache2/conf/server-opts.txt

# Copy files to the server setup directory.
cp -p %_builddir/conf/apache2.conf %instroot/apache2/conf/
cp -p %_builddir/conf/archive-log-files %instroot/apache2/etc/
cp -p %_builddir/conf/httpd %instroot/apache2/etc/init.d/
cp -p %i/etc/profile.d/dependencies-setup.sh %instroot/apache2/etc/startenv.d/00-core-server.sh
touch %instroot/apache2/logs/start_stop.log

%post
# Relocate files.
CFG=$RPM_INSTALL_PREFIX/apache2/conf
perl -p -i -e "s|%instroot|$RPM_INSTALL_PREFIX|g"	\
  $RPM_INSTALL_PREFIX/%pkgrel/etc/profile.d/*-*.*sh	\
  $RPM_INSTALL_PREFIX/apache2/conf/apache2.conf		\
  $RPM_INSTALL_PREFIX/apache2/etc/init.d/httpd		\
  $RPM_INSTALL_PREFIX/apache2/etc/startenv.d/00-core-server.sh

# Set ServerName.
H=$(hostname -f)
if [ -r /etc/grid-security/hostcert.pem ]; then
  CN=$(openssl x509 -noout -subject -in /etc/grid-security/hostcert.pem 2>/dev/null | sed 's|.*/CN=||')
  case $CN in *.*.* ) H=$CN ;; esac
fi

echo "Adjusting ServerName to $H."
perl -p -i -e 's/^ServerName (\S+)$/ServerName '$H'/g' $CFG/apache2.conf

# Deter attempts to modify installed files locally.
chmod a-w $RPM_INSTALL_PREFIX/apache2/conf/apache2.conf
chmod a-w $RPM_INSTALL_PREFIX/apache2/etc/archive-log-files
chmod a-w $RPM_INSTALL_PREFIX/apache2/etc/init.d/httpd
chmod a-w $RPM_INSTALL_PREFIX/apache2/etc/startenv.d/00-core-server.sh

%files
%i/
%dir %instroot/apache2
%dir %instroot/apache2/etc
%dir %instroot/apache2/etc/init.d
%dir %instroot/apache2/etc/startenv.d
%dir %instroot/apache2/var
%dir %instroot/apache2/logs
%dir %instroot/apache2/conf
%dir %instroot/apache2/htdocs
%dir %instroot/apache2/apps.d
%attr(444,-,-) %config %instroot/apache2/conf/apache2.conf
%attr(444,-,-) %instroot/apache2/etc/startenv.d/00-core-server.sh
%attr(555,-,-) %instroot/apache2/etc/init.d/httpd
%attr(555,-,-) %instroot/apache2/etc/archive-log-files
%attr(644,-,-) %instroot/apache2/logs/start_stop.log
%config %instroot/apache2/conf/server-opts.txt
