### RPM external python-ldap 2.3.5
## INITENV +PATH PYTHONPATH %i/lib/python`echo $PYTHON_VERSION | cut -f1,2 -d.`/site-packages

Source: http://voxel.dl.sourceforge.net/sourceforge/python-ldap/python-ldap-%{realversion}.tar.gz
Patch0: python-ldap-2.3.5-gcc44
Requires: python openssl openldap

%define isslc6 %(case %cmsplatf in (slc6*) echo true ;; (*) echo false ;; esac)

%if "%isslc6" == "true"
# On SLC6 we build missing Cyrus SASL.
Requires: cyrus-sasl
%endif

%prep
%setup -q -n %n-%{realversion}
%patch0 -p1

%build

# XXX:
# Paths in library_dirs (setup.cfg) are hardcoded into RPATH dynamic section
# attribute of the binary. Shared libraries are first searched in RPATH paths
# before LD_LIBRARY_PATH paths. More information in 'distutils' Python package
# source code.

# Modify setup.cfg with proper include/libs dirs
# ROOT_CYRUS_SASL should be included only on SLC6.
# SLC5 has the library by default

CYRUS_SASL_ROOT=${CYRUS_SASL_ROOT:-"/usr"}
sed -i'' "s:\(library_dirs =\)\(.*\):\1 ${CYRUS_SASL_ROOT}\/lib ${OPENSSL_ROOT}\/lib ${PYTHON_ROOT}\/lib ${OPENLDAP_ROOT}\/lib:g" setup.cfg
sed -i'' "s:\(include_dirs = \)\(.*\):\1 ${CYRUS_SASL_ROOT}\/include\/sasl ${OPENSSL_ROOT}\/include ${PYTHON_ROOT}\/include ${OPENLDAP_ROOT}\/include:g" setup.cfg

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

