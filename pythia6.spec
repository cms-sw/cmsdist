### RPM external pythia6 426
Source: http://cern.ch/service-spi/external/MCGenerators/distribution/%{n}/%{n}-%{realversion}-src.tgz

%define keep_archives true

%prep
%setup -q -n %{n}/%{realversion}

# Update to detect aarch64 and ppc64le
rm -f ./config/config.{sub,guess}
%get_config_sub ./config/config.sub
%get_config_guess ./config/config.guess
chmod +x ./config/config.{sub,guess}

%ifos darwin
  LD="$(which gcc)" LDFLAGS='-Wl,-commons,use_dylibs -Wl,-flat_namespace'  \
%endif
  ./configure --disable-shared --enable-static --with-hepevt=4000 F77="$(which gfortran) -fPIC"

perl -p -i -e 's|^CC=.*$|CC="gcc -fPIC"|' libtool

%build
make CFLAGS="-fPIC -fcommon"
make install

%install
tar -c lib include | tar -x -C %i

%post
%{relocateConfig}include/Makefile
%{relocateConfig}lib/lib*.la
