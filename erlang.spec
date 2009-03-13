### RPM external erlang R12B-5
Source: http://erlang.org/download/otp_src_R12B-5.tar.gz
Requires: gcc openssl

%prep
%setup -n otp_src_%{realversion}

%build
LANG=C; export LANG
./configure
make

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

