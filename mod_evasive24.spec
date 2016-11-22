### RPM external mod_evasive24 1.10.1
#Source: https://www.zdziarski.com/blog/wp-content/uploads/2010/02/mod_evasive_%realversion.tar.gz
Source: https://fossies.org/linux/www/apache_httpd_modules/old/mod_evasive_%realversion.tar.gz
Patch: mod_evasive_dn

# See some docs at
# https://mbrownnyc.wordpress.com/technology-solutions/create-a-secure-linux-web-server/install-and-configure-mod_evasive-for-apache-2-4-x/
# https://www.zdziarski.com/blog/?page_id=442

# Requires apache2
Requires: apache24

%prep
%setup -n mod_evasive
%patch -p1

%build
$APACHE24_ROOT/bin/apxs -c mod_evasive20.c
pwd
ls

%install
mkdir -p %i/modules
cp -f .libs/* %i/modules
rm %i/modules/*.la
cp -f *.la %i/modules

mkdir -p %i/conf
cat << \EOF > %i/conf/mod_evasive.conf
LoadModule evasive_module %i/modules/mod_evasive.so
# Additional configuration bits go here.
EOF

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

# Strip libraries, we are not going to debug them.
%define strip_files %i/{lib,modules}

# Look up documentation online.
%define drop_files %i/man

%post
%{relocateConfig}conf/mod_evasive.conf
%{relocateConfig}etc/profile.d/dependencies-setup.*sh
