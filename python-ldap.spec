### RPM external python-ldap 2.3.5
## INITENV +PATH PYTHONPATH %i/lib/python`echo $PYTHON_VERSION | cut -f1,2 -d.`/site-packages

Source: http://voxel.dl.sourceforge.net/sourceforge/python-ldap/python-ldap-%{realversion}.tar.gz
Patch0: python-ldap-2.3.5-gcc44
Requires: python openssl openldap

%prep
%setup -q -n %n-%{realversion}
%patch0 -p1

%build
mkdir -p sasl2lib
ln -s /usr/lib/libsasl2.so.2.0.19 sasl2lib/libsasl2.so

perl -p -i -e 's|/usr/local/openldap-2.3/|$ENV{OPENLDAP_ROOT}/|; s|(library_dirs = .*)|$1 /usr/lib/sasl2 %{_builddir}/%n-%{realversion}/sasl2lib $ENV{OPENSSL_ROOT}/lib|;' setup.cfg
python setup.py build
%install
python setup.py install --prefix=%i

# SCRAM ToolBox toolfile
mkdir -p %i/etc/scram.d
cat << \EOF_TOOLFILE >%i/etc/scram.d/%n.xml
  <tool name="%n" version="%v">
    <info url="http://python-ldap.sourceforge.net/"/>
    <client>
      <environment name="PYTHON_LDAP_BASE" default="%i"/>
      <environment name="PYTHON_LDAP_PYPATH" default="$PYTHON_LDAP_BASE/lib/python@PYTHONV@/site-packages"/>
    </client>
    <runtime name="PYTHONPATH" value="$PYTHON_LDAP_PYPATH" type="path"/>
    <use name="openssl"/>
    <use name="openldap"/>
    <use name="python"/>
  </tool>
EOF_TOOLFILE

export PYTHONV=$(echo $PYTHON_VERSION | cut -f1,2 -d.)
perl -p -i -e 's|\@([^@]*)\@|$ENV{$1}|g' %i/etc/scram.d/*

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
%{relocateConfig}etc/scram.d/%n.xml
# The relocation below is also needed for dependencies
%{relocateConfig}etc/profile.d/dependencies-setup.sh
%{relocateConfig}etc/profile.d/dependencies-setup.csh

