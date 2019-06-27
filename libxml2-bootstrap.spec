### RPM external libxml2-bootstrap 2.9.1
Source: ftp://xmlsoft.org/libxml2/libxml2-%{realversion}.tar.gz
%define strip_files %{i}/lib/lib* %{i}/bin/{xmlcatalog,xmllint}
%define drop_files %{i}/share/{man,doc,gtk-doc}

Requires: xz-bootstrap

%prep
%setup -n libxml2-%{realversion}

%build
./configure --disable-static --prefix=%{i} --build="%{_build}" \
            --host="%{_host}" --with-zlib \
            --with-lzma="${XZ_BOOTSTRAP_ROOT}" --without-python
make %{makeprocesses}

%install
make install
rm -rf %{i}/lib/pkgconfig
rm -rf %{i}/lib/*.{l,}a

%post
%{relocateConfig}bin/xml2-config
%{relocateConfig}lib/xml2Conf.sh
# bla bla
