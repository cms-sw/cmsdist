### RPM external jimmy 4.2

Requires: herwig
Source: http://service-spi.web.cern.ch/service-spi/external/MCGenerators/distribution/%{n}-%{realversion}-src.tgz
Patch0: jimmy-4.2-gfortran
Patch1: jimmy-4.2-macosx

%if "%(echo %cmsos | grep osx >/dev/null && echo true)" == "true"
Requires: gfortran-macosx
%endif

%prep
%setup -q -n %{n}/%{realversion}
case %gccver in
  4.*)
%patch0 -p0
%patch1 -p3
  ;;
esac


%build
# NOTE: only in recent architectures we build static libraries. 
case %cmsplatf in
  slc*_*_gcc4[0123]*) ;;
  *) PLATF_CONFIG_OPTS="--enable-static --disable-shared" ;;
esac

./configure $PLATF_CONFIG_OPTS --with-herwig=$HERWIG_ROOT
# Looks like ./configure does not do all it should do to have our
# version of herwig picked up at link time.
# Workaround until they fix the GENESER makefiles is to define
# the variable and use it directly inside "Makeshared".
make HERWIG_ROOT=$HERWIG_ROOT

%install
tar -c lib include | tar -x -C %i
find %i/lib/archive -name "*.a" -exec mv {} %i/lib \;
rm -rf %i/lib/archive
