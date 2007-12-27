### RPM external glimpse 4.18.5-CMS19
Source: http://webglimpse.net/trial/glimpse-%{realversion}.tar.gz

%prep
%setup -n glimpse-%realversion
%build
./configure --prefix=%{i} 
# Turn off this part, it causes problems for 32-bit-on-64-bit and is only
# needed for webglimpse
perl -p -i -e "s|dynfilters||g" Makefile
make 

%install
make install
# SCRAM ToolBox toolfile
mkdir -p %i/etc/scram.d
cat << \EOF_TOOLFILE >%i/etc/scram.d/%n
<doc type=BuildSystem::ToolDoc version=1.0>
<Tool name=glimpse version=%v>
<Client>
 <Environment name=GLIMPSE_BASE default="%i"></Environment>
</Client>
<Runtime name=PATH value="$GLIMPSE_BASE/bin" type=path>
</Tool>
EOF_TOOLFILE

%post
%{relocateConfig}etc/scram.d/%n
