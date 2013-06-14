### RPM external apache 2.0.59
%define downloadn httpd
Source: http://apache.osuosl.org/httpd/httpd-%v.tar.gz
Requires: zlib openssl expat
%prep
%setup -n %{downloadn}-%{v}

%build
./configure CFLAGS="-I$EXPAT_ROOT/include" \
            LDFLAGS="-L$EXPAT_ROOT/lib" \
            --prefix=%{i} \
            --with-z=$LIBZ_ROOT \
            --with-ssl=$OPENSSL_ROOT \
            --enable-ssl \
            --enable-rewrite \
            --enable-so

mkdir -p %i/conf.d

make %makeprocesses
%install
%initenv
mkdir -p %{i}
true || exit 0
make install

echo 'Include '"%i/conf.d/"'*.conf' >> \
  %i/conf/httpd.conf


%post
%{relocateConfig}conf/highperformance.conf
%{relocateConfig}conf/highperformance-std.conf
%{relocateConfig}conf/httpd.conf
%{relocateConfig}conf/httpd-std.conf
%{relocateConfig}conf/ssl.conf
%{relocateConfig}conf/ssl-std.conf
%{relocateConfig}include/ap_config_auto.h
%{relocateConfig}include/ap_config_layout.h
%{relocateConfig}bin/apachectl
%{relocateConfig}bin/apr-config
%{relocateConfig}bin/apu-config
%{relocateConfig}bin/apxs
%{relocateConfig}bin/envvars
%{relocateConfig}bin/envvars-std
