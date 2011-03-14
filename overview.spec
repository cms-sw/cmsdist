### RPM cms overview 6.0.2
## INITENV +PATH PYTHONPATH %i/lib/python`echo $PYTHON_VERSION | cut -d. -f 1,2`/site-packages
## INITENV +PATH PYTHONPATH %i/xlib/python`echo $PYTHON_VERSION | cut -d. -f 1,2`/site-packages

%define svn svn://svn.cern.ch/reps/CMSDMWM/Monitoring/tags/%{realversion}
Source: %{svn}?scheme=svn+ssh&strategy=export&module=Monitoring&output=/src.tar.gz
Requires: cherrypy py2-cheetah yui py2-cx-oracle py2-pil py2-matplotlib rotatelogs

%prep
# Unpack sources.
%setup -n Monitoring

# Build
%build
python setup.py build_system -s Overview

# Install
%install
mkdir -p %i/etc/profile.d %i/{x,}{bin,lib,include,data}
python setup.py install_system -s Overview --prefix=%i
find %i -name '*.egg-info' -exec rm {} \;

# Generate dependencies-setup.{sh,csh} so init.{sh,csh} picks full environment.
: > %i/etc/profile.d/dependencies-setup.sh
: > %i/etc/profile.d/dependencies-setup.csh
for tool in $(echo %{requiredtools} | sed -e's|\s+| |;s|^\s+||'); do
  root=$(echo $tool | tr a-z- A-Z_)_ROOT; eval r=\$$root
  if [ X"$r" != X ] && [ -r "$r/etc/profile.d/init.sh" ]; then
    echo "test X\$$root != X || . $r/etc/profile.d/init.sh" >> %i/etc/profile.d/dependencies-setup.sh
    echo "test X\$$root != X || source $r/etc/profile.d/init.csh" >> %i/etc/profile.d/dependencies-setup.csh
  fi
done

# Generate an env.sh which sets a few things more than init.sh.
(echo ". %i/etc/profile.d/init.sh;"
 echo "export PATH=%i/xbin:\$PATH;"
 echo "export LD_LIBRARY_PATH=%i/xlib:\$LD_LIBRARY_PATH;"
 echo "export YUI_ROOT='$YUI_ROOT';"
 echo "export MONITOR_ROOT='%i';") > %i/etc/profile.d/env.sh

%post
%{relocateConfig}etc/profile.d/{env,dep*}.*sh
