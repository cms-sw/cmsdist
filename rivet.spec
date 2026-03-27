### RPM external rivet 4.1.2
## INCLUDE cpp-standard
## INCLUDE microarch_flags
## INITENV +PATH PYTHON3PATH %{i}/${PYTHON3_LIB_SITE_PACKAGES}
## OLD GENSER Source: http://cern.ch/service-spi/external/MCGenerators/distribution/rivet/rivet-%{realversion}-src.tgz
Source: git+https://gitlab.com/hepcedar/rivet.git?obj=main/%{n}-%{realversion}&export=%{n}-%{realversion}&output=/%{n}-%{realversion}.tgz
Source99: scram-tools.file/tools/eigen/env
Patch0: rivet-duplicate-libs
Patch1: rivet-postrelease

Requires: hepmc3 fastjet fastjet-contrib yoda hdf5 highfive onnxruntime
BuildRequires: python3 py3-cython autotools

%prep
%setup -n %{n}-%{realversion}
%patch0 -p1
%patch1 -p1

%build
source %{_sourcedir}/env
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

autoreconf -fiv

#disable building Rivet with OpenMP as it crash executables due to static TLS blocks
%ifarch aarch64
sed -i -e 's|^ax_openmp_flags=".*"|ax_openmp_flags="none"|' ./configure
%endif
CXXFLAGS="-std=c++%{cms_cxx_standard} $CMS_EIGEN_CXX_FLAGS %{selected_microarch}"
sed -i "/_pow10 only defined for positive powers/d" include/Rivet/Tools/ParticleIdUtils.hh
# Disable ONNX download
sed -e '/wget -P pluginONNX/,/exit 1);/d' \
    -e 's/\.download_onnx_data:/.download_onnx_data:\n\ttouch .download_onnx_data/' analyses/Makefile.am

PYTHON=$(which python3) \
./configure --disable-silent-rules --prefix=%{i} --with-hepmc=${HEPMC3_ROOT} \
            --with-fastjet=${FASTJET_ROOT} --with-fjcontrib=${FASTJET_CONTRIB_ROOT} --with-yoda=${YODA_ROOT} \
            --disable-doxygen --with-pic --enable-h5 --enable-onnxrt=${ONNXRUNTIME_ROOT} \
            CXX="mpicxx" CPPFLAGS="-I${BOOST_ROOT}/include" CXXFLAGS="${CXXFLAGS}"
# The following hack insures that the bins with the library linked explicitly
# rather than indirectly, as required by the gold linker
perl -p -i -e "s|LIBS = $|LIBS = -lHepMC3|g" bin/Makefile
make %{makeprocesses} all

%install
make install
sed -i -e 's|^#!.*python.*|#!/usr/bin/env python3|' %{i}/bin/*

%post
%{relocateConfig}bin/rivet-config
%{relocateConfig}bin/rivet-build
