### RPM external gsl 2.6
Source: ftp://ftp.gnu.org/gnu/%{n}/%{n}-%{realversion}.tar.gz
Requires: OpenBLAS
%define runpath_opts -m cblas
%define keep_archives true

%prep
%setup -n %{n}-%{realversion}

# Update config.{guess,sub} scripts to detect aarch64 and ppc64le
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

%build
CFLAGS="-O2" ./configure --prefix=%{i} --with-pic
case $(uname)-$(uname -m) in
  Darwin-i386)
   perl -p -i -e "s|#define HAVE_DARWIN_IEEE_INTERFACE 1|/* option removed */|" config.h;; 
esac

make %{makeprocesses}

%install
make install

# Remove pkg-config to avoid rpm-generated dependency on /usr/bin/pkg-config
# which we neither need nor use at this time.
rm -rf %{i}/lib/pkgconfig

# Strip libraries, we are not going to debug them.
%define strip_files %{i}/lib
rm -f %{i}/lib/*.la
# Look up documentation online.
%define drop_files %{i}/share

#Move away gslcblas library to make sure that one one links against it.
#We want to use the OpenBlas implementation
#https://github.com/cms-sw/cmsdist/issues/5528
mkdir %i/cblas
mv  %i/lib/libgslcblas* %i/cblas/

#Make sure openblas library exists
test ${OPENBLAS_ROOT}/lib/libopenblas.%{dynamic_lib_ext}
sed -i -e "s|-lgslcblas|-L${OPENBLAS_ROOT}/lib -lopenblas|" %{i}/bin/gsl-config

%post
%{relocateConfig}bin/gsl-config
