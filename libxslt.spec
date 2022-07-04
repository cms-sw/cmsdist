### RPM external libxslt 1.1.35

Source0: https://github.com/GNOME/%{n}/archive/refs/tags/v%{realversion}.tar.gz

Requires: libxml2 zlib xz
BuildRequires: autotools
%prep
%setup -n %{n}-%{realversion}

%build
autoreconf -ivf
./configure \
  --prefix=%{i} \
  --with-libxml-prefix=$LIBXML2_ROOT \
  --without-crypto --without-python
make

%install
make install

%post
%{relocateConfig}bin/xslt-config
