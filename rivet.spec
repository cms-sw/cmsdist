### RPM external rivet 2.5.4
## OLD GENSER Source: http://cern.ch/service-spi/external/MCGenerators/distribution/rivet/rivet-%{realversion}-src.tgz
Source: http://lcgpackages.web.cern.ch/lcgpackages/tarFiles/sources/MCGeneratorsTarFiles/Rivet-%{realversion}.tar.bz2

Requires: hepmc fastjet gsl yoda
BuildRequires: python py2-cython

Patch0: rivet-1.4.0

%prep
## OLD GENSER: %setup -n rivet/%{realversion}
%setup -n Rivet-%{realversion}
%patch0 -p0

# Update config.{guess,sub} to detect aarch64 and ppc64le
rm -f %{_tmppath}/config.{sub,guess}
curl -L -k -s -o %{_tmppath}/config.guess 'http://git.savannah.gnu.org/gitweb/?p=config.git;a=blob_plain;f=config.guess;hb=HEAD'
curl -L -k -s -o %{_tmppath}/config.sub 'http://git.savannah.gnu.org/gitweb/?p=config.git;a=blob_plain;f=config.sub;hb=HEAD'
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

# fix regex to handle case with two -L statements (from gsl w/ openblas)
sed -i 's/\.\*-L\\s\*(\\S+)\.\*/-L(\\S+)/' pyext/setup.py.in

./configure --disable-silent-rules --prefix=%{i} --with-hepmc=${HEPMC_ROOT} \
            --with-fastjet=${FASTJET_ROOT} --with-gsl=$GSL_ROOT --with-yoda=${YODA_ROOT} \
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
