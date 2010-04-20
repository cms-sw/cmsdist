### RPM external elementtree 1.2.6
Source: http://effbot.org/downloads/%n-%realversion-20050316.zip
Requires: python
 
%prep
%setup -n %n-%realversion-20050316

%build
%install
python setup.py install --prefix=%i/share

# SCRAM ToolBox toolfile
mkdir -p %i/etc/scram.d
cat << \EOF_TOOLFILE >%i/etc/scram.d/%n.xml
  <tool name="%n" version="%v">
    <info url="http://www.boost.org"/>
    <client>
      <environment name="ELEMENTTREE_BASE" default="%i"/>
      <environment name="ELEMENTTREE_PYPATH" default="$ELEMENTTREE_BASE/share/lib/python@PYTHONV@/site-packages"/>
    </client>
    <runtime name="PYTHONPATH" value="$ELEMENTTREE_PYPATH" type="path"/>
    <use name="gccxml"/>
    <use name="python"/>
  </tool>
EOF_TOOLFILE

export PYTHONV=$(echo $PYTHON_VERSION | cut -f1,2 -d.)
perl -p -i -e 's|\@([^@]*)\@|$ENV{$1}|g' %i/etc/scram.d/*

%post
%{relocateConfig}etc/scram.d/%n.xml
