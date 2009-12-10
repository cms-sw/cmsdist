### RPM external libpng 1.2.10-CMS19
Source: http://riksun.riken.go.jp/pub/pub/Linux/slackware/slackware-current/source/l/libpng/%{n}-%{realversion}.tar.bz2
Requires: zlib
%prep
%setup -n %n-%{realversion}
 
%build
./configure --prefix=%{i}
make %makeprocesses

%install
make install
# SCRAM ToolBox toolfile
mkdir -p %i/etc/scram.d
cat << \EOF_TOOLFILE >%i/etc/scram.d/%n
<doc type=BuildSystem::ToolDoc version=1.0>
<Tool name=%n version=%v>
<info url="http://www.libpng.org/"></info>
<lib name=png>
<Client>
 <Environment name=LIBPNG_BASE default="%i"></Environment>
 <Environment name=LIBDIR default="$LIBPNG_BASE/lib"></Environment>
 <Environment name=INCLUDE default="$LIBPNG_BASE/include"></Environment>
</Client>
<Use name=zlib>
</Tool>
EOF_TOOLFILE

%post
%{relocateConfig}bin/libpng-config
%{relocateConfig}bin/libpng12-config
%{relocateConfig}lib/libpng.la
%{relocateConfig}lib/libpng12.la
%{relocateConfig}lib/pkgconfig/libpng.pc
%{relocateConfig}lib/pkgconfig/libpng12.pc
%{relocateConfig}etc/scram.d/%n
