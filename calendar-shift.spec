### RPM cms calendar-shift 1
## INITENV SET SAMPLE_MYAPP_ENV_VAR %i/somedir/or/name

Requires: python cherrypy py2-pyopenssl py2-pyxml
Source: svn://svnweb.cern.ch/guest/cmsawstats/Utils?scheme=http&module=Utils&output=/awstat_utils.tgz

%prep
%setup -n Utils

%build

%install
cp -rp %_builddir/Utils/* %i/

# Dependencies environment
rm -rf %i/etc/profile.d
mkdir -p %i/etc/profile.d
for x in %pkgreqs; do
  case $x in /* ) continue ;; esac
  p=%{instroot}/%{cmsplatf}/$(echo $x | sed 's/\([^+]*\)+\(.*\)+\([A-Z0-9].*\)/\1 \2 \3/' | tr ' ' '/')
  echo ". $p/etc/profile.d/init.sh" >> %i/etc/profile.d/dependencies-setup.sh
  echo "source $p/etc/profile.d/init.csh" >> %i/etc/profile.d/dependencies-setup.csh
done

%post
# Relocation for dependencies environment
%{relocateConfig}etc/profile.d/dependencies-setup.sh
%{relocateConfig}etc/profile.d/dependencies-setup.csh

