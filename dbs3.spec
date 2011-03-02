### RPM cms dbs3 3.0.4
## INITENV +PATH PYTHONPATH %i/Server/Python/src
## INITENV SET DBS3_SERVER_ROOT %i/Server/Python

%define cvstag %(echo %{realversion} | sed 's/[.]/_/g; s/^/DBS_/')

Requires: wmcore-webtools wmcore-db-oracle py2-cjson py2-mysqldb rotatelogs
Source: svn://svn.cern.ch/reps/CMSDMWM/DBS/tags/%cvstag?scheme=svn+ssh&strategy=export&module=DBS3&output=/%{n}.tar.gz

%prep
%setup -n DBS3

%build

%install
cp -rp %_builddir/DBS3/* %i/

#----------------------------------------
## Generates the script used to setup dbs3
cat << \EOF > %i/setup.sh

if [ -z "$DBS3_ROOT" ]; then
       source ./etc/profile.d/init.sh
fi

EOF

#--------------------------------------------------------------------
# The following lines (including relocation ones in the post section) 
# are necessary to correctly setup the environment.
rm -rf %i/etc/profile.d
# Copy dependencies to dependencies-setup.sh
mkdir -p %i/etc/profile.d
for x in %pkgreqs; do
  case $x in /* ) continue ;; esac
  p=%{instroot}/%{cmsplatf}/$(echo $x | sed 's/\([^+]*\)+\(.*\)+\([A-Z0-9].*\)/\1 \2 \3/' | tr ' ' '/')
  echo ". $p/etc/profile.d/init.sh" >> %i/etc/profile.d/dependencies-setup.sh
  echo "source $p/etc/profile.d/init.csh" >> %i/etc/profile.d/dependencies-setup.csh
done

%post
%{relocateConfig}etc/profile.d/dependencies-setup.*sh

%files
%i/
%exclude %i/src
%exclude %i/Server/JAVA
%exclude %i/Server/Http
