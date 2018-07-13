### RPM external thrift 0.11.0
Source: http://xenia.sote.hu/ftp/mirrors/www.apache.org/%{n}/%{realversion}/%{n}-%{realversion}.tar.gz

Requires: zlib boost python

%prep
%setup -n %{n}-%{realversion}

%build
./configure --prefix=%{i} --with-boost=${BOOST_ROOT} --with-python=${PYTHON_ROOT} --without-lua --without-nodejs --without-ruby --with-zlib=${ZLIB_ROOT}
make -j %{makeprocesses}

%install
make install
