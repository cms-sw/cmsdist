### RPM external libjpg 8b
Source: http://www.ijg.org/files/jpegsrc.v%{realversion}.tar.gz

%prep
%setup -n jpeg-%realversion

%build
./configure --prefix=%{i} --enable-shared --enable-static

make %makeprocesses
%install
mkdir -p %{i}/lib
mkdir -p %{i}/bin
mkdir -p %{i}/include
mkdir -p %{i}/man/man1
make install

# SCRAM ToolBox toolfile
mkdir -p %i/etc/scram.d
cat << \EOF_TOOLFILE >%i/etc/scram.d/%n
<doc type=BuildSystem::ToolDoc version=1.0>
<Tool name=%n version=%v>
<info url="http://www.ijg.org/"></info>
<lib name=jpeg>
<Client>
 <Environment name=LIBJPEG_BASE default="%i"></Environment>
 <Environment name=LIBDIR default="$LIBJPEG_BASE/lib"></Environment>
 <Environment name=INCLUDE default="$LIBJPEG_BASE/include"></Environment>
</Client>
</Tool>
EOF_TOOLFILE

%post
%{relocateConfig}lib/libjpeg.la
%{relocateConfig}etc/scram.d/%n
