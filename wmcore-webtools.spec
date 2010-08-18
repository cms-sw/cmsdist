### RPM cms wmcore-webtools 1

Requires: wmcore cherrypy py2-cheetah py2-openid yui

%prep
%build
%install
mkdir -p %i/bin

# setup dependencies environment
rm -rf %i/etc/profile.d
mkdir -p %i/etc/profile.d
for x in %pkgreqs; do
  case $x in /* ) continue ;; esac
  p=%{instroot}/%{cmsplatf}/$(echo $x | sed 's/\([^+]*\)+\(.*\)+\([A-Z0-9].*\)/\1 \2 \3/' | tr ' ' '/')
  echo ". $p/etc/profile.d/init.sh" >> %i/etc/profile.d/dependencies-setup.sh
  echo "source $p/etc/profile.d/init.csh" >> %i/etc/profile.d/dependencies-setup.csh
done

%post
# The relocation is also needed because of dependencies
%{relocateConfig}etc/profile.d/dependencies-setup.sh
%{relocateConfig}etc/profile.d/dependencies-setup.csh

# setup approripate links
. $RPM_INSTALL_PREFIX/%{pkgrel}/etc/profile.d/init.sh
if [ -n "${WMCORE_ROOT}" ]; then
	ln -s ${WMCORE_ROOT}/lib/WMCore/WebTools/Root.py $RPM_INSTALL_PREFIX/%{pkgrel}/bin/Root.py
fi

