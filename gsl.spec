### RPM external gsl 2.2.1
## INITENV SET GSL_CBLAS_LIB -L${OPENBLAS_ROOT}/lib -lopenblas
Source: ftp://ftp.gnu.org/gnu/%{n}/%{n}-%{realversion}.tar.gz
Requires: OpenBLAS

%define keep_archives true

%prep
%setup -n %{n}-%{realversion}

# Update config.{guess,sub} scripts to detect aarch64 and ppc64le
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
mv  %i/lib/*gslcblas* %i/cblas

%post
%{relocateConfig}bin/gsl-config
