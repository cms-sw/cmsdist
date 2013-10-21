### RPM external jimmy 4.2
%define mic %(case %cmsplatf in (*_mic_*) echo true;; (*) echo false;; esac)
%if "%mic" == "true"
Requires: icc
%endif
Requires: herwig
Source: http://service-spi.web.cern.ch/service-spi/external/MCGenerators/distribution/%{n}/%{n}-%{realversion}-src.tgz
Patch0: jimmy-4.2-gfortran
Patch1: jimmy-4.2-macosx

%define keep_archives true
%if "%(case %cmsplatf in (osx*_*_gcc421) echo true ;; (*) echo false ;; esac)" == "true"
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
case %cmsos in
  slc5_*_gcc4[01234]*) ;;
  *) BUILD_PRODUCT=lib_archive ;;
esac
./configure $PLATF_CONFIG_OPTS --with-herwig=$HERWIG_ROOT

%if "%mic" == "true"
sed -i -e 's|F77 *=.*|F77 = ifort -mmic|' config.mk
%endif
# Looks like ./configure does not do all it should do to have our
# version of herwig picked up at link time.
# Workaround until they fix the GENESER makefiles is to define
# the variable and use it directly inside "Makeshared".
make HERWIG_ROOT=$HERWIG_ROOT $BUILD_PRODUCT

%install
tar -c lib include | tar -x -C %i
find %i/lib/archive -name "*.a" -exec mv {} %i/lib \;
rm -rf %i/lib/archive

