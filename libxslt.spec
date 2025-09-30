### RPM external libxslt 1.1.42

Source: https://gitlab.gnome.org/GNOME/libxslt/-/archive/v%{realversion}/libxslt-v%{realversion}.tar.gz

Requires: libxml2
BuildRequires: autotools
%prep
%setup -n %{n}-v%{realversion}

%build

LDFLAGS="-L$LIBXML2_ROOT/lib -lxml2" \
./autogen.sh \
  --prefix=%{i} \
  --disable-silent-rules \
  --with-libxml-prefix=$LIBXML2_ROOT \
  --with-libxml-include-prefix=$LIBXML2_ROOT/include/libxml2 \
  --with-libxml-libs-prefix=$LIBXML2_ROOT/lib \
  --without-crypto --without-python
make %{makeprocesses} VERBOSE=1

%install
make install

%post
%{relocateConfig}bin/xslt-config
%{relocateConfig}include/libxslt/xsltconfig.h
%{relocateConfig}lib/xsltConf.sh
