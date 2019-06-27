### RPM external fitsio 3.350

%define download_version %(echo "%{realversion}" | tr -d '.')

Source: ftp://heasarc.gsfc.nasa.gov/software/%{n}/c/cfitsio%{download_version}.tar.gz

%define keep_archives true

%prep
%setup -n cfitsio

%build
./configure \
  --prefix=%{i} \
  --enable-reentrant \
  --enable-sse2

make %{makeprocesses}

%install
make install
# bla bla
