### RPM external erlang R12B-5
Source: http://erlang.org/download/otp_src_R12B-5.tar.gz
Requires: gcc openssl
Provides: libc.so.6(GLIBC_PRIVATE)(64bit)

%prep
%setup -n otp_src_R12B-5

%build
LANG=C; export LANG
if [ `uname -m` != 'x86_64' ]; then
    LDFLAGS=-A`uname -m` ./configure --prefix=%i
    LDFLAGS=-A`uname -m` make
else
    ./configure --prefix=%i
    make
fi

%install
make install
# SCRAM ToolBox toolfile
mkdir -p %i/etc/scram.d
cat << \EOF_TOOLFILE >%i/etc/scram.d/%n
<doc type=BuildSystem::ToolDoc version=1.0>
<Tool name=Erlang version=%v>
<lib name=erlang>
<client>
 <Environment name=ERLANG_BASE default="%i"></Environment>
 <Environment name=INCLUDE default="$ERLANG_BASE/include"></Environment>
 <Environment name=LIBDIR  default="$ERLANG_BASE/lib"></Environment>
</client>
<Runtime name=PATH value="$ERLANG_BASE/bin" type=path>
</Tool>
EOF_TOOLFILE

%post
%{relocateConfig}etc/scram.d/%n
%{relocateConfig}etc/profile.d/dependencies-setup.sh
%{relocateConfig}etc/profile.d/dependencies-setup.csh

