### RPM external sip 4.8.2
## INITENV +PATH PYTHONPATH %i/lib/python2.4/site-packages
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
cat << \EOF_TOOLFILE >%i/etc/scram.d/sip
<doc type=BuildSystem::ToolDoc version=1.0>
<Tool name=sip version=%v>
<info url="http://www.riverbankcomputing.co.uk/software/sip/intro"></info>
<Client>
 <Environment name=SIP_BASE default="%i"></Environment>
</Client>
<Runtime name=PYTHONPATH value="$SIP_BASE/lib/python2.4/site-packages" type=path>
<use name="python">
</Tool>
EOF_TOOLFILE

%post
%{relocateConfig}etc/scram.d/sip
