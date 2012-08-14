### RPM cms alertscollector 0.1-rc1

Source0: git://github.com/zdenekmaxa/WMCore?obj=alertscollector/HEAD&export=%n&output=/%n.tar.gz
# realversion can be taken from above, but has to correspond to a GIT tag
#Source0: git://github.com/dmwm/WMCore?obj=master/%realversion&export=%n&output=/%n.tar.gz
# download tip of a branch (problem with added username and username's hash ...)
#Source0: https://github.com/zdenekmaxa/WMCore/tarball/alertscollector

Requires: python couchapp
# (cherrypy) bug introduced in 
# https://github.com/dmwm/WMCore/commit/2922d23d3f980caa65899f443f1a8f67a0cb8a1c
# setup_test depends on that but it's not necessary
# sphinx is also necessary for build try to produce documentation
BuildRequires: cherrypy py2-sphinx

%prep
%setup -b 0 -n %n


%build
python setup.py build_system -s alertscollector


%install
# cannot stat alertscollector directory
#cp -r alertscollector/* %i
python setup.py install_system -s alertscollector --prefix=%i
find %i -name '*.egg-info' -exec rm {} \;


# Generate dependencies-setup.{sh,csh} so init.{sh,csh} picks full environment.
# Should remove this too - no dependencies
# yes, it's ok
#mkdir -p %i/etc/profile.d
#: > %i/etc/profile.d/dependencies-setup.sh
#: > %i/etc/profile.d/dependencies-setup.csh
#for tool in $(echo %{requiredtools} | sed -e's|\s+| |;s|^\s+||'); do
#  root=$(echo $tool | tr a-z- A-Z_)_ROOT; eval r=\$$root
#  if [ X"$r" != X ] && [ -r "$r/etc/profile.d/init.sh" ]; then
#    echo "test X\$$root != X || . $r/etc/profile.d/init.sh" >> %i/etc/profile.d/dependencies-setup.sh
#    echo "test X\$$root != X || source $r/etc/profile.d/init.csh" >> %i/etc/profile.d/dependencies-setup.csh
#  fi
#done

%post
# remove (or leave post empty)
# yes, it's ok
#%{relocateConfig}etc/profile.d/dependencies-setup.*sh
