### RPM cms overview 6.0.7
## INITENV +PATH PATH %i/xbin
## INITENV +PATH %{dynamic_path_var} %i/xlib
## INITENV +PATH PYTHONPATH %i/${PYTHON_LIB_SITE_PACKAGES}
## INITENV +PATH PYTHONPATH %i/x${PYTHON_LIB_SITE_PACKAGES}

%define webdoc_files %{installroot}/%{pkgrel}/doc/
%define svn svn://svn.cern.ch/reps/CMSDMWM/Monitoring/tags/%{realversion}
Source: %{svn}?scheme=svn+ssh&strategy=export&module=Monitoring&output=/src.tar.gz
Requires: cherrypy py2-cheetah yui py2-cx-oracle py2-pil py2-matplotlib py2-pycurl
Requires: py2-cjson rotatelogs py2-sphinx

%prep
# Unpack sources.
%setup -n Monitoring
perl -p -i -e "s{<VERSION>}{%{realversion}}g" doc/*/conf.py

# Build
%build
python setup.py build_system -s Overview

# Install
%install
mkdir -p %i/etc/profile.d %i/{x,}{bin,lib,include,data} %i/{x,}$PYTHON_LIB_SITE_PACKAGES
python setup.py install_system -s Overview --prefix=%i
find %i -name '*.egg-info' -exec rm {} \;

# Generate dependencies-setup.{sh,csh} so init.{sh,csh} picks full environment.
: > %i/etc/profile.d/dependencies-setup.sh
: > %i/etc/profile.d/dependencies-setup.csh
for tool in $(echo %{requiredtools} | sed -e's|\s+| |;s|^\s+||'); do
  root=$(echo $tool | tr a-z- A-Z_)_ROOT; eval r=\$$root
  if [ X"$r" != X ] && [ -r "$r/etc/profile.d/init.sh" ]; then
    echo "test X\$$root != X || . $r/etc/profile.d/init.sh" >> %i/etc/profile.d/dependencies-setup.sh
    echo "test X\$?$root = X1 || source $r/etc/profile.d/init.csh" >> %i/etc/profile.d/dependencies-setup.csh
  fi
done

# Generate an env.sh which sets a few things more than init.sh.
(echo ". %i/etc/profile.d/init.sh;"
 echo "export YUI_ROOT;"
 echo "export MONITOR_ROOT='%i';") > %i/etc/profile.d/env.sh

%post
%{relocateConfig}etc/profile.d/{env,dep*}.*sh

%files
%{installroot}/%{pkgrel}/
%exclude %{installroot}/%{pkgrel}/doc

## SUBPACKAGE webdoc
