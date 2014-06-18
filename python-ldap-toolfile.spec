### RPM external python-ldap-toolfile 2.0
Requires: python-ldap
%prep

%build

%install

mkdir -p %i/etc/scram.d
cat << \EOF_TOOLFILE >%i/etc/scram.d/python-ldap.xml
<tool name="python-ldap" version="@TOOL_VERSION@">
  <info url="http://python-ldap.sourceforge.net/"/>
  <client>
    <environment name="PYTHON_LDAP_BASE" default="@TOOL_ROOT@"/>
    <environment name="PYTHON_LDAP_PYPATH" default="$PYTHON_LDAP_BASE/lib/python@PYTHONV@/site-packages"/>
  </client>
  <runtime name="PYTHONPATH" value="$PYTHON_LDAP_PYPATH" type="path"/>
  <use name="openssl"/>
  <use name="openldap"/>
  <use name="python"/>
</tool>
EOF_TOOLFILE

export PYTHONV=$(echo $PYTHON_VERSION | cut -f1,2 -d.)

## IMPORT scram-tools-post
