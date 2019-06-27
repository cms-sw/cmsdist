### RPM external libxml2 2.9.1
Source: ftp://xmlsoft.org/%{n}/%{n}-%{realversion}.tar.gz
%define strip_files %{i}/lib/lib* %{i}/bin/{xmlcatalog,xmllint}
%define drop_files %{i}/share/{man,doc,gtk-doc}

Requires: zlib xz

%prep
%setup -n %{n}-%{realversion}

%build
./configure --disable-static --prefix=%{i} --build="%{_build}" \
            --host="%{_host}" --with-zlib="${ZLIB_ROOT}" \
            --with-lzma="${XZ_ROOT}" --without-python
make %{makeprocesses}

%install
make install
rm -rf %{i}/lib/pkgconfig
rm -rf %{i}/lib/*.{l,}a

%post
%{relocateConfig}bin/xml2-config
%{relocateConfig}lib/xml2Conf.sh
# bla bla
