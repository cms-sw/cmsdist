### RPM external libxml2 2.9.1
Source: ftp://xmlsoft.org/libxml2/libxml2-%realversion.tar.gz
%define strip_files %{i}/lib/lib* %{i}/bin/{xmlcatalog,xmllint}
%define drop_files %{i}/share/{man,doc,gtk-doc}

Requires: zlib

%prep
%setup -n libxml2-%realversion

%build
./configure --disable-static --prefix=%{i} --build="%{_build}" \
            --host="%{_host}" --with-zlib="${ZLIB_BOOTSTRAP_ROOT}" --without-python
make %{makeprocesses}

%install
make install

%post
%{relocateConfig}bin/xml2-config
%{relocateConfig}lib/xml2Conf.sh
