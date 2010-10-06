### RPM external icu4c 4_0_1
Source: http://download.icu-project.org/files/icu4c/4.0.1/%n-%realversion-src.tgz

%prep
%setup -n icu

%build
cd source
chmod +x runConfigureICU configure install-sh
./runConfigureICU Linux --prefix=%i
make

%install
cd source
make install

export ICU_INSTALL_DIR=%i
cat %i/bin/icu-config | \
    sed "s,$ICU_INSTALL_DIR,\$ICU4C_ROOT,g" \
        > %i/bin/icu-config.new
mv %i/bin/icu-config.new %i/bin/icu-config
chmod a+x %i/bin/icu-config

