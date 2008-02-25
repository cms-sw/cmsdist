### RPM cms apache2-conf 1.0
# Configuration for additional apache2 modules
Source: none
Requires:  mod_perl2 mod_python apache2

%prep
%build
%install
mkdir -p %i/conf %i/bin

# FIXME: make sure that mod_perl2.conf/mod_python.conf are actually called that way. 
# FIXME: autogenerate from Requires.
cat << \EOF > %i/conf/apache2.conf
Include @APACHE2_ROOT@/conf/httpd.conf
Include @MOD_PERL2_ROOT@/conf/mod_perl2.conf
Include @MOD_PYTHON_ROOT@/conf/mod_python.conf
# Additional configuration bits go here.
EOF

cat << \EOF > %i/bin/httpd
#!/bin/sh
@APACHE2_ROOT@/bin/httpd -f %i/conf/apache2.conf {1+"$@"}
EOF


perl -p -i -e "s|\@APACHE2_ROOT\@|$APACHE2_ROOT|g;
               s|\@MOD_PERL2_ROOT\@|$MOD_PERL2_ROOT|g;
               s|\@MOD_PYTHON_ROOT\@|$MOD_PYTHON_ROOT|g;" %i/conf/apache2.conf %i/bin/httpd

%post
%{relocateConfig}bin/httpd
%{relocateConfig}conf/apache2.conf
