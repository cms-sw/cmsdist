### RPM external libevent 1.4.9
Source: http://www.monkey.org/~provos/libevent-%{realversion}-stable.tar.gz

%prep 
%setup -n libevent-%realversion-stable

%build
./configure --prefix=%i
make

%install
make install

# SCRAM ToolBox toolfile
mkdir -p %i/etc/scram.d
cat << \EOF_TOOLFILE >%i/etc/scram.d/%n
<doc type=BuildSystem::ToolDoc version=1.0>
<Tool name=%n version=%v>
<lib name=z>
<client>
 <Environment name=LIBEVENT_BASE default="%i"></Environment>
 <Environment name=INCLUDE default="$LIBEVENT_BASE/include"></Environment>
 <Environment name=LIBDIR  default="$LIBEVENT_BASE/lib"></Environment>
</client>
</Tool>
EOF_TOOLFILE

%post
%{relocateConfig}etc/scram.d/%n

