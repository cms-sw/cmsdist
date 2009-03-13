### RPM external spidermonkey 1.8.0-rc1
Source: http://ftp.mozilla.org/pub/mozilla.org/js/js-%realversion.tar.gz

%prep
%setup -n %n-%{realversion}

%build
cd js/src
make -f Makefile.ref

%install
make install
# SCRAM ToolBox toolfile
mkdir -p %i/etc/scram.d
cat << \EOF_TOOLFILE >%i/etc/scram.d/%n
<doc type=BuildSystem::ToolDoc version=1.0>
<Tool name=Spidermonkey version=%v>
<lib name=spidermonkey>
<client>
 <Environment name=SPIDERMONKEY_BASE default="%i"></Environment>
 <Environment name=INCLUDE default="$SPIDERMONKEY_BASE/include"></Environment>
 <Environment name=LIBDIR  default="$SPIDERMONKEY_BASE/lib"></Environment>
</client>
<Runtime name=PATH value="$SPIDERMONKEY_BASE/bin" type=path>
</Tool>
EOF_TOOLFILE

%post
%{relocateConfig}etc/scram.d/%n

