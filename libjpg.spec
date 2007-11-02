### RPM external libjpg 6b-CMS18
Source: ftp://ftp.uu.net/graphics/jpeg/jpegsrc.v%{realversion}.tar.gz
Source1: config.sub-amd64
Patch0: libjpg-config.sub
Patch1: libjpg-config.guess
Patch2: libjpg-ltmain.sh
Patch3: libjpg-ltconfig
Patch4: libjpg-makefile.cfg
%prep
%setup -n jpeg-%realversion
%patch0
%patch1
%patch2
%patch3
%patch4


%build
# libjpg ships with an old version of config.sub. 
if [ "$(uname -m)" == "x86_64" ] || [ "$(uname -m)" == "ppc64" ]
then
cp %{_sourcedir}/config.sub-amd64 config.sub
fi
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
