### RPM external libxml2-bootstrap 2.7.7
%define downloadv %(echo %{realversion} | cut -d"_" -f1)
Source: ftp://xmlsoft.org/libxml2/libxml2-%{downloadv}.tar.gz
%define strip_files %{i}/lib/lib* %{i}/bin/{xmlcatalog,xmllint}
%define drop_files %{i}/share/{man,doc,gtk-doc}

Requires: zlib-bootstrap

%prep
%setup -n libxml2-%{downloadv}

%build
./configure --disable-static --prefix=%{i} --build="%{_build}" \
            --host="%{_host}" --with-zlib="${ZLIB_BOOTSTRAP_ROOT}" --without-python
make %{makeprocesses}

%install
make install
rm -rf %{i}/lib/pkgconfig
rm -rf %{i}/lib/*.{l,}a

%post
%{relocateConfig}bin/xml2-config
%{relocateConfig}lib/xml2Conf.sh
