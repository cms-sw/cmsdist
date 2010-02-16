### RPM external readline 6.0
Source: ftp://ftp.cwru.edu/pub/bash/%n-%realversion.tar.gz

%prep
%setup -n %n-%realversion

%build
./configure --prefix=%i
make %makeprocesses

%install
make install

# SCRAM ToolBox toolfile
mkdir -p %i/etc/scram.d
cat << \EOF_TOOLFILE >%i/etc/scram.d/%n
<doc type=BuildSystem::ToolDoc version=1.0>
<Tool name=%n version=%v>
<lib name=z>
<client>
 <Environment name=READLINE_BASE default="%i"></Environment>
 <Environment name=INCLUDE default="$READLINE_BASE/include"></Environment>
 <Environment name=LIBDIR  default="$READLINE_BASE/lib"></Environment>
</client>
</Tool>
EOF_TOOLFILE

%post
%{relocateConfig}etc/scram.d/%n
