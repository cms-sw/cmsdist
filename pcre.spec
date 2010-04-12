### RPM external pcre 7.9
Source: http://downloads.sourceforge.net/%n/%n-%{realversion}.tar.bz2
Requires: bz2lib

%prep
%setup -n %n-%{realversion}
%build
./configure --enable-unicode-properties --enable-pcregrep-libz --enable-pcregrep-libbz2 --prefix=%i
make

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

## IMPORT common-install

%post
%{relocateConfig}bin/pcre-config
%{relocateConfig}etc/scram.d/%n
## IMPORT common-post

