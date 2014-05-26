### RPM cms frontend 4.3
Source: http://www.nikhef.nl/~janjust/proxy-verify/grid-proxy-verify.c
Requires: apache-setup mod_perl2 p5-apache2-modssl p5-compress-zlib p5-json-xs
Requires: p5-digest-hmac py2-cx-oracle oracle-env sqlite

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
