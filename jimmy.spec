### RPM external jimmy 4.2

Requires: herwig
Source: http://service-spi.web.cern.ch/service-spi/external/MCGenerators/distribution/%{n}/%{n}-%{realversion}-src.tgz
Patch0: jimmy-4.2-configure-update

%define keep_archives true

%prep
%setup -q -n %{n}/%{realversion}
%patch0 -p2

%build
./configure $PLATF_CONFIG_OPTS --with-herwig=$HERWIG_ROOT
# Looks like ./configure does not do all it should do to have our
# version of herwig picked up at link time.
# Workaround until they fix the GENESER makefiles is to define
# the variable and use it directly inside "Makeshared".
make HERWIG_ROOT=$HERWIG_ROOT lib_archive

%install
tar -c lib include | tar -x -C %i
find %i/lib/archive -name "*.a" -exec mv {} %i/lib \;
rm -rf %i/lib/archive

# bla bla
