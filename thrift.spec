### RPM external thrift 0.10.0
Source: http://xenia.sote.hu/ftp/mirrors/www.apache.org/%{n}/%{realversion}/%{n}-%{realversion}.tar.gz

Requires: zlib

%prep
%setup -n %{n}-%{realversion}

%build
./configure --prefix=%{i} --without-boost --without-python --without-lua --without-nodejs --without-ruby --with-zlib=${ZLIB_ROOT}
make -j %{makeprocesses}

%install
make install
