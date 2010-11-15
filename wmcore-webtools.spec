### RPM cms wmcore-webtools 1

Requires: wmcore cherrypy py2-cheetah yui

%prep
%build
%install
mkdir -p %i/bin

# Generate dependencies-setup.{sh,csh} so init.{sh,csh} picks full environment.
mkdir -p %i/etc/profile.d
: > %i/etc/profile.d/dependencies-setup.sh
: > %i/etc/profile.d/dependencies-setup.csh
for tool in $(echo %{requiredtools} | sed -e's|\s+| |;s|^\s+||'); do
  root=$(echo $tool | tr a-z- A-Z_)_ROOT; eval r=\$$root
  if [ X"$r" != X ] && [ -r "$r/etc/profile.d/init.sh" ]; then
    echo "test X\$$root != X || . $r/etc/profile.d/init.sh" >> %i/etc/profile.d/dependencies-setup.sh
    echo "test X\$$root != X || source $r/etc/profile.d/init.csh" >> %i/etc/profile.d/dependencies-setup.csh
  fi
done

%post
%{relocateConfig}etc/profile.d/dependencies-setup.*sh

# setup approripate links
. $RPM_INSTALL_PREFIX/%{pkgrel}/etc/profile.d/init.sh
if [ -n "${WMCORE_ROOT}" ]; then
	ln -s ${WMCORE_ROOT}/lib/WMCore/WebTools/Root.py $RPM_INSTALL_PREFIX/%{pkgrel}/bin/Root.py
fi

