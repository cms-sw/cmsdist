### RPM external libffi 3.5.2
## INITENV +PATH LD_LIBRARY_PATH %{i}/lib64

Source: https://github.com/libffi/libffi/archive/refs/tags/v%{realversion}.tar.gz
BuildRequires: autotools gmake

%prep
%setup -n %{n}-%{realversion}
rm -f config.{sub,guess}
%get_config_guess config.guess
%get_config_sub   config.sub
autoreconf -fiv

%build
CFLAGS="-Wno-deprecated-declarations" \
  ./configure \
  --prefix=%{i} \
  --enable-portable-binary \
  --disable-dependency-tracking \
  --disable-static --disable-docs

make %{makeprocesses}

%install
make %{makeprocesses} install

rm -rf %{i}/lib
rm -rf %{i}/lib64/*.la

%define drop_files %{i}/share
