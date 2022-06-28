### RPM external libxslt 1.1.33

Source0: http://xmlsoft.org/sources/%{n}-%{realversion}.tar.gz

Requires: libxml2 zlib xz
BuildRequires: autotools
%prep
%setup -n %{n}-%{realversion}

%build
./autogen.sh \
  --prefix=%{i} \
  --with-libxml-prefix=$LIBXML2_ROOT \
  --with-libxml-include-prefix=$LIBXML2_ROOT/include \
  --with-libxml-libs-prefix=$LIBXML2_ROOT/lib \
  --without-crypto --without-python
make

%install
make install

%post
%{relocateConfig}bin/xslt-config
