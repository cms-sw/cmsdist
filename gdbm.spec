### RPM external gdbm 1.10
Source: http://ftp.gnu.org/gnu/%{n}/%{n}-%{realversion}.tar.gz

%prep
%setup -n %{n}-%{realversion}

%build
# Update to detect aarch64 and ppc64le
rm -f ./build-aux/config.{sub,guess}
%get_config_sub ./build-aux/config.sub
%get_config_guess ./build-aux/config.guess
chmod +x ./build-aux/config.{sub,guess}

./configure \
  --enable-libgdbm-compat \
  --prefix=%{i} \
  --disable-dependency-tracking \
  --disable-nls \
  --disable-rpath

make %{makeprocesses}

%define strip_files %{i}/lib
%define drop_files %{i}/share
