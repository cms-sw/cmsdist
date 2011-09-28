### RPM external icu4c 4_0_1
Source: http://download.icu-project.org/files/icu4c/4.0.1/%n-%realversion-src.tgz
%ifos darwin
%define make gnumake
%define platf MacOSX
%else
%define make make
%define platf Linux
%endif

%prep
%setup -n icu
perl -p -i -e 's/^#elif$/#else/' source/layoutex/ParagraphLayout.cpp

%build
cd source
chmod +x runConfigureICU configure install-sh
./runConfigureICU %platf --prefix=%i
%make %makeprocesses

%install
cd source
%make install

export ICU_INSTALL_DIR=%i
cat %i/bin/icu-config | \
    sed "s,$ICU_INSTALL_DIR,\$ICU4C_ROOT,g" \
        > %i/bin/icu-config.new
mv %i/bin/icu-config.new %i/bin/icu-config
chmod a+x %i/bin/icu-config

# Strip libraries, we are not going to debug them.
%define strip_files %i/lib

# Look up documentation online.
%define drop_files %i/man
