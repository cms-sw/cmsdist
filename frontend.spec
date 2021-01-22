### RPM cms frontend 5.0
Source: http://www.nikhef.nl/~janjust/proxy-verify/grid-proxy-verify.c
Requires: apache24-setup mod_perl24 mod_evasive24 p5-apache24-modssl p5-compress-zlib p5-json-xs
Requires: p5-digest-hmac py2-cx-oracle oracle-env sqlite

# changes to support x509 parsing from traefik headers
Requires: p5-crypt-X509 p5-uri p5-inline-c p5-inline-cpp simple-proxy-utils

# changes to support x509-scitoken-issuer in cmsweb frontend
Requires: mod_wsgi24 mod_gridsite24 x509-scitokens-issuer py2-flask
# changes to support CERN SSO
Requires: py2-flask-sso
# changes to support OAuth
Requires: py2-flask-sqlalchemy py2-flask-login py2-rauth py2-argparse py2-rauth

%prep

%build
gcc -o %_builddir/grid-proxy-verify %_sourcedir/grid-proxy-verify.c \
  -I$OPENSSL_ROOT/include -L$OPENSSL_ROOT/lib -lssl -lcrypto -ldl

%install
mkdir -p %i/{bin,etc/env.d,etc/profile.d}
ln -sf ../profile.d/init.sh %i/etc/env.d/10-frontend.sh
cp -p %_builddir/grid-proxy-verify %i/bin/

# Generate dependencies-setup.{sh,csh} so init.{sh,csh} picks full environment.
: > %i/etc/profile.d/dependencies-setup.sh
: > %i/etc/profile.d/dependencies-setup.csh
for tool in $(echo %{requiredtools} | sed -e's|\s+| |;s|^\s+||'); do
  root=$(echo $tool | tr a-z- A-Z_)_ROOT; eval r=\$$root
  if [ X"$r" != X ] && [ -r "$r/etc/profile.d/init.sh" ]; then
    echo "test X\$$root != X || . $r/etc/profile.d/init.sh" >> %i/etc/profile.d/dependencies-setup.sh
    echo "test X\$?$root = X1 || source $r/etc/profile.d/init.csh" >> %i/etc/profile.d/dependencies-setup.csh
  fi
done

# Clean up unnecessary environment before starting the server.
cat > %i/etc/env.d/99-env-cleanup.sh <<- \EOF
        case $(uname) in Darwin ) unset LD_LIBRARY_PATH ;; * ) unset DYLD_FALLBACK_LIBRARY_PATH ;; esac
EOF

%post
%{relocateConfig}etc/profile.d/dependencies-setup.*sh
