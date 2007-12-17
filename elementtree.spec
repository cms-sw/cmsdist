### RPM external elementtree 1.2.6
Source: http://effbot.org/downloads/%n-%realversion-20050316.zip
Requires: python

%prep
%setup -n %n-%realversion-20030511

%build
%install
python setup.py install --prefix=%i/share

# SCRAM ToolBox toolfile
mkdir -p %i/etc/scram.d
cat << \EOF_TOOLFILE >%i/etc/scram.d/%n
<doc type=BuildSystem::ToolDoc version=1.0>
<Tool name=%n version=%v>
<info url="http://www.boost.org"></info>
<Client>
 <Environment name=ELEMENTTREE_BASE default="%i"></Environment>
 <Environment name=ELEMENTTREE_PYPATH default="$ELEMENTTREE_BASE/share/lib/python2.4/site-packages"></Environment>
</Client>
<use name=gccxml>
<use name=python>
<Runtime name=PYTHONPATH value="$ELEMENTTREE_PYPATH" type=path>
</Tool>
EOF_TOOLFILE

%post
%{relocateConfig}etc/scram.d/%n
