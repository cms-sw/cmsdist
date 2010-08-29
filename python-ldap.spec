### RPM external python-ldap 2.3.5
## INITENV +PATH PYTHONPATH %i/lib/python`echo $PYTHON_VERSION | cut -f1,2 -d.`/site-packages

Source: http://voxel.dl.sourceforge.net/sourceforge/python-ldap/python-ldap-%{realversion}.tar.gz
Patch0: python-ldap-2.3.5-gcc44
Requires: python openssl openldap

%prep
%setup -q -n %n-%{realversion}
%patch0 -p1

%build

perl -p -i -e 's|/usr/local/openldap-2.3/|$ENV{OPENLDAP_ROOT}/|; s|(library_dirs = .*)|$1 /usr/lib/sasl2 $ENV{OPENSSL_ROOT}/lib|;' setup.cfg
python setup.py build
%install
python setup.py install --prefix=%i

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
%{relocateConfig}etc/profile.d/dependencies-setup.sh
%{relocateConfig}etc/profile.d/dependencies-setup.csh

