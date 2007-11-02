### RPM external sqlite 3.4.0-CMS18
Source: http://service-spi.web.cern.ch/service-spi/external/tarFiles/%{n}-%{realversion}.tar.gz
Patch1: sqlite_%{realversion}_readline_for_32bit_on_64bit_build

%prep
%setup -n %n-%{realversion}
# The following hack and patch are there because the libreadline.so soft
# link is missing from the 32-bit compatibility area on the 64-bit build
# machines and apparently they don't have a -devel build with it. It
# definitely should be reviewed at some point.
%patch1 -p1 
mkdir .libs
ln -s /usr/lib/libreadline.so.4.3 .libs/libreadline.so

%build
./configure --prefix=%i --disable-tcl
make %makeprocesses

%install
make install
# SCRAM ToolBox toolfile
mkdir -p %i/etc/scram.d
cat << \EOF_TOOLFILE >%i/etc/scram.d/%n
<doc type=BuildSystem::ToolDoc version=1.0>
<Tool name=%n version=%v>
<lib name=sqlite3>
<Client>
 <Environment name=SQLITE_BASE default="%i"></Environment>
 <Environment name=LIBDIR default="$SQLITE_BASE/lib"></Environment>
 <Environment name=BINDIR default="$SQLITE_BASE/bin"></Environment>
 <Environment name=INCLUDE default="$SQLITE_BASE/include"></Environment>
</Client>
<Runtime name=PATH value="$BINDIR" type=path>
</Tool>
EOF_TOOLFILE

%post
%{relocateConfig}etc/scram.d/%n
