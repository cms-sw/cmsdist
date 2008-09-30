### RPM cms apache2-conf 1.9b
# Configuration for additional apache2 modules
%define cvsserver cvs://:pserver:anonymous@cmscvs.cern.ch:2401/cvs_server/repositories/CMSSW?passwd=AA_:yZZ3e&strategy=export&nocache=true
Source0: %cvsserver&module=COMP/WEBTOOLS/Configuration&export=conf&tag=-rSERVER_CONF_1_9b&output=/config.tar.gz
Source1: %cvsserver&module=COMP/WEBTOOLS/WelcomePages&export=htdocs&tag=-rSERVER_CONF_1_9b&output=/htdocs.tar.gz
Requires:  mod_perl2 mod_python apache2

%prep
%setup -T -b 0 -n conf
%setup -D -T -b 1 -n htdocs

%build
%install

# Make directory for various resources of this package
mkdir -p %i/bin %i/logs %i/var %i/conf %i/startenv.d %i/htdocs %i/tools
mkdir -p %i/apps.d %i/rewrites.d %i/ssl_rewrites.d

cp -p %_builddir/conf/*.conf                 %i/conf
cp -p %_builddir/conf/rewrites.d/*.conf      %i/rewrites.d
cp -p %_builddir/conf/ssl_rewrites.d/*.conf  %i/ssl_rewrites.d
cp -p %_builddir/conf/apps.d/*.conf          %i/apps.d
cp -p %_builddir/conf/testme		     %i/tools
cp -rp %_builddir/htdocs/*                   %i/htdocs

# Make a server start script, with our environment.
sed 's/^  //' << EOF > %i/bin/httpd
  #!/bin/sh
  for file in %i/startenv.d/*.sh; do
    [ -f \$file ] || continue
    . \$file
  done
  exec $APACHE2_ROOT/bin/httpd -f %i/conf/apache2.conf \${1+"\$@"}
EOF
chmod +x %i/bin/httpd

# Replace template variables in configuration files with actual paths.
perl -p -i -e "
  s|\@SERVER_ROOT\@|%i|g;
  s|\@APACHE2_ROOT\@|$APACHE2_ROOT|g;
  s|\@MOD_PERL2_ROOT\@|$MOD_PERL2_ROOT|g;
  s|\@MOD_PYTHON_ROOT\@|$MOD_PYTHON_ROOT|g;" \
  %i/*/*.conf

# Generate dependencies-setup.{sh,csh}.
rm -rf %i/etc/profile.d
mkdir -p %i/etc/profile.d
: > %{i}/etc/profile.d/dependencies-setup.sh
: > %{i}/etc/profile.d/dependencies-setup.csh
for tool in `echo %{requiredtools} | sed -e's|\s+| |;s|^\s+||'`; do
  eval toolroot=\$$(echo $tool | tr a-z- A-Z_)_ROOT
  if [ X"${toolroot:+set}" = Xset ] && [ -d "$toolroot" ]; then
    echo ". $toolroot/etc/profile.d/init.sh" >> %i/etc/profile.d/dependencies-setup.sh
    echo "source $toolroot/etc/profile.d/init.csh" >> %i/etc/profile.d/dependencies-setup.csh
  fi
done

# Copy dependencies to the environment setup directory.
cp -p %i/etc/profile.d/dependencies-setup.sh %i/startenv.d/apache2.sh

%post
%{relocateConfig}bin/httpd
%{relocateConfig}*/*.conf
%{relocateConfig}startenv.d/*.sh
%{relocateConfig}etc/profile.d/*-*.*sh
