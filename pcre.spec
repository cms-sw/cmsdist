### RPM external pcre 4.4-CMS19
Source: http://downloads.sourceforge.net/%n/%n-%{realversion}.tar.bz2

%prep
%setup -n %n-%{realversion}

%install
make install
# SCRAM ToolBox toolfile
mkdir -p %i/etc/scram.d
cat << \EOF_TOOLFILE >%i/etc/scram.d/%n
<doc type=BuildSystem::ToolDoc version=1.0>
<Tool name=%n version=%v>
<info url="http://www.pcre.org"></info>
<lib name=pcre>
<Client>
 <Environment name=PCRE_BASE default="%i"></Environment>
 <Environment name=LIBDIR default="$PCRE_BASE/lib"></Environment>
 <Environment name=INCLUDE default="$PCRE_BASE/include"></Environment>
</Client>
</Tool>
EOF_TOOLFILE

%post
%{relocateConfig}bin/pcre-config
%{relocateConfig}etc/scram.d/%n
