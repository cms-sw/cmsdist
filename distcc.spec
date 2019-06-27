### RPM external distcc 3.2rc1
Source: https://distcc.googlecode.com/files/distcc-%{realversion}.tar.gz
Requires: python

Patch0: distcc-gcc7

%prep
%setup -n %{n}-%{realversion}
%patch0 -p1

%build
# Update to detect aarch64 and ppc64le
rm -f ./config.{sub,guess}
curl -L -k -s -o ./config.sub 'http://git.savannah.gnu.org/gitweb/?p=config.git;a=blob_plain;f=config.sub;hb=HEAD'
curl -L -k -s -o ./config.guess 'http://git.savannah.gnu.org/gitweb/?p=config.git;a=blob_plain;f=config.guess;hb=HEAD'
chmod +x ./config.{sub,guess}

./configure \
  --prefix %{i} \
  --without-gtk \
  --without-gnome \
  --without-avahi \
  CFLAGS="-O2 -Wno-unused-but-set-variable -Wno-unused-local-typedefs -Wno-unused-parameter -Wno-unused-const-variable" \
  CC="$(which gcc)" \
  PYTHON=${PYTHON_ROOT}/bin/python

make %{makeprocesses}

%install
make install
ln -sf distcc %{i}/bin/c++
ln -sf distcc %{i}/bin/cc
ln -sf distcc %{i}/bin/gcc
ln -sf distcc %{i}/bin/gfortran
%post
%{relocateConfig}bin/pump
# bla bla
