### RPM external rivet 3.0.1
## INITENV +PATH PYTHON27PATH %{i}/${PYTHON_LIB_SITE_PACKAGES}
## INITENV +PATH PYTHON3PATH %{i}/${PYTHON3_LIB_SITE_PACKAGES}
## OLD GENSER Source: http://cern.ch/service-spi/external/MCGenerators/distribution/rivet/rivet-%{realversion}-src.tgz
Source: http://lcgpackages.web.cern.ch/lcgpackages/tarFiles/sources/MCGeneratorsTarFiles/Rivet-%{realversion}.tar.bz2

Requires: hepmc fastjet fastjet-contrib yoda
BuildRequires: python py2-cython py2-setuptools

Patch0: rivet-1.4.0
Patch1: rivet-weightnames

%prep
## OLD GENSER: %setup -n rivet/%{realversion}
%setup -n Rivet-%{realversion}
%patch0 -p0
%patch1 -p1

# Install latex packages from doc directory
# Des not fix missing SIUnits on lxplus7 yet, expected for Rivet 3.0.2
for sty in ./doc/*.sty; do mkdir -p ./data/texmf/tex/latex/${sty:6:-4}; done
for sty in ./doc/*.sty; do cp ${sty} ./data/texmf/tex/latex/${sty:6:-4}; done

# Update config.{guess,sub} to detect aarch64 and ppc64le
rm -f %{_tmppath}/config.{sub,guess}
%get_config_guess %{_tmppath}/config.guess
%get_config_sub %{_tmppath}/config.sub
for CONFIG_GUESS_FILE in $(find $RPM_BUILD_DIR -name 'config.guess')
do
  rm -f $CONFIG_GUESS_FILE
  cp %{_tmppath}/config.guess $CONFIG_GUESS_FILE
  chmod +x $CONFIG_GUESS_FILE
done
for CONFIG_SUB_FILE in $(find $RPM_BUILD_DIR -name 'config.sub')
do
  rm -f $CONFIG_SUB_FILE
  cp %{_tmppath}/config.sub $CONFIG_SUB_FILE
  chmod +x $CONFIG_SUB_FILE
done

case %{cmsplatf} in
  slc6*) sed -i -e 's#^ *OPENMP_CXXFLAGS=.*#OPENMP_CXXFLAGS=#' configure ;;
esac
sed -i -e "s#if test x\$ASCIIDOC != x#if false#g" configure
autoreconf --install
./configure --disable-silent-rules --prefix=%{i} --with-hepmc=${HEPMC_ROOT} \
            --with-fastjet=${FASTJET_ROOT} --with-fjcontrib=${FASTJET_CONTRIB_ROOT} --with-yoda=${YODA_ROOT} \
            --disable-doxygen --disable-pdfmanual --with-pic \
            CXX="$(which g++)" CPPFLAGS="-I${BOOST_ROOT}/include"

# The following hack insures that the bins with the library linked explicitly
# rather than indirectly, as required by the gold linker
perl -p -i -e "s|LIBS = $|LIBS = -lHepMC|g" bin/Makefile
%build
make %{makeprocesses} all 
%install
make install 

%post
%{relocateConfig}bin/rivet-config
%{relocateConfig}bin/rivet-buildplugin
