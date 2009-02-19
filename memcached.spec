### RPM external memcached 1.2.6
Source: http://www.danga.com/memcached/dist/memcached-%{realversion}.tar.gz
Requires: libevent

%prep 
%setup -n memcached-%realversion

%build
source $LIBEVENT_ROOT/etc/profile.d/init.sh
./configure --with-libevent=$LIBEVENT_ROOT --prefix=%i
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
 <Environment name=MEMCACHED_BASE default="%i"></Environment>
 <Environment name=INCLUDE default="$MEMCACHED_BASE/include"></Environment>
 <Environment name=LIBDIR  default="$MEMCACHED_BASE/lib"></Environment>
</client>
</Tool>
EOF_TOOLFILE

%post
%{relocateConfig}etc/scram.d/%n

