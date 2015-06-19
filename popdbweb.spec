### RPM cms popdbweb 0.3.3
Source: https://github.com/dmwm/DDM/archive/popdb-web-%realversion.tar.gz
Requires: python oracle oracle-env django py2-cx-oracle py2-pycurl
Requires: apache-setup mod_wsgi mod_perl2 apache2 

%prep
%setup -n DDM-popdb-web-%realversion

%build

%install
mkdir -p %i/etc/{env,profile}.d
(cd DataPopularity/popdb.web
sed -i -e "s#/var/www/DjangoProjects/CMSDataPopularity#%i/#g" setup.cfg
sed -i -e "\#/var/www/html#d" -e "\#/etc/httpd/conf.d#d" setup.py
sed -i -e "\#onfile#d" lib/Apps/popularity/views/data_collection.py
sed -i -e "s#Apps.popCommon.utils.confSettings#confSettings#g" \
  lib/Apps/popCommon/database/popCommonDB.py                   \
  lib/Apps/xrdPopularity/urls.py                               \
  lib/Apps/victorinterface/replicaCombiner.py                  \
  lib/Apps/victorinterface/replicaPopularity.py                \
  lib/Apps/victorinterface/replicaPopularityBase.py            \
  lib/Apps/popularity/urls.py                                  \
  lib/Apps/popularity/utils/PopularityParams.py                \
  lib/Apps/popularity/database/popDB.py                        \
  lib/Apps/popularity/views/data_collection.py                 \
  lib/Apps/popularity/views/rendering_views.py
sed -i -e "28,43d" lib/Apps/popCommon/template/base.html
python setup.py install)
find %i -name '*.egg-info' -exec rm {} \;

# cleanup config files
rm -f %i/etc/conf{,_secret}.ini %i/lib/{settings,manage,popularity_wsgi}.py*
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
