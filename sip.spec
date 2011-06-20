### RPM external sip 4.8.2
## INITENV +PATH PYTHONPATH %i/lib/python$(echo $PYTHON_VERSION |cut -d. -f 1,2)/site-packages
Source: http://www.riverbankcomputing.co.uk/static/Downloads/sip4/sip-%realversion.tar.gz
Requires: python
%prep
%setup -n sip-%realversion 

%build
python ./configure.py -v %i/share -b %i/bin -d %i/lib/python`echo $PYTHON_VERSION | cut -d. -f 1,2`/site-packages -e %i/include
make %makeprocesses

%install
make install

mkdir -p %i/etc/scram.d
cat << \EOF_TOOLFILE >%i/etc/scram.d/%n.xml
  <tool name="%n" version="%v">
    <info url="http://www.riverbankcomputing.co.uk/software/sip/intro"/>
    <client>
      <environment name="SIP_BASE" default="%i"/>
    </client>
    <runtime name="PYTHONPATH" value="$SIP_BASE/lib/python@PYTHONV@/site-packages" type="path"/>
    <use name="python"/>
  </tool>
EOF_TOOLFILE

export PYTHONV=$(echo $PYTHON_VERSION | cut -f1,2 -d.)
perl -p -i -e 's|\@([^@]*)\@|$ENV{$1}|g' %i/etc/scram.d/*

%post
%{relocateConfig}etc/scram.d/%n.xml
%{relocateConfig}lib/python2.6/site-packages/sipconfig.py
