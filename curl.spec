### RPM external curl 7.15.3-CMS19
Source: http://curl.haxx.se/download/%n-%realversion.tar.gz

%prep
%setup -n %n-%{realversion}

%build
./configure --prefix=%i --without-libidn --disable-crypto-auth --without-ssl
make %makeprocesses

%install
make install
# SCRAM ToolBox toolfile
mkdir -p %i/etc/scram.d
cat << \EOF_TOOLFILE >%i/etc/scram.d/%n
<doc type=BuildSystem::ToolDoc version=1.0>
<Tool name=Curl version=%v>
<lib name=curl>
<client>
 <Environment name=CURL_BASE default="%i"></Environment>
 <Environment name=INCLUDE default="$CURL_BASE/include"></Environment>
 <Environment name=LIBDIR  default="$CURL_BASE/lib"></Environment>
</client>
<Runtime name=PATH value="$CURL_BASE/bin" type=path>
</Tool>
EOF_TOOLFILE

%post
%{relocateConfig}bin/curl-config
%{relocateConfig}etc/scram.d/%n
