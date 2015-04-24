### RPM cms victorweb 0.3.2
Source: https://github.com/dmwm/DDM/archive/victor-web-%realversion.tar.gz
Requires: python oracle oracle-env py2-cx-oracle django
Requires: apache-setup mod_wsgi mod_perl2 apache2 

%prep
%setup -n DDM-victor-web-%realversion

%build
sed -i "s;/media2/;/victor/media/;g" Victor/victor.monitoring.cms/templates/*

%install
mkdir -p %i/etc/{env,profile}.d
(cd Victor/victor.monitoring.cms
sed -i -e "s#/var/www/DjangoProjects/victor#%i#g" setup.cfg
sed -i -e "\#/var/www/html#d" -e "\#/etc/httpd/conf.d#d" setup.py
sed -i -e "\#tracking.html#d" templates/*
sed -i -e "s#victor.views#views#g" lib/urls.py
python setup.py install)
find %i -name '*.egg-info' -exec rm {} \;
rm -f %i/{settings,victor_wsgi,config,manager}.py* %i/templates/tracking.html

# Generate dependencies-setup.{sh,csh} so init.{sh,csh} picks full environment.
ln -sf ../profile.d/init.sh %i/etc/env.d/11-datasvc.sh
mkdir -p %i/etc/profile.d/
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
