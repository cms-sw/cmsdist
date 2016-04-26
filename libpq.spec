### RPM external libpq 9.4.5

Source: https://ftp.postgresql.org/pub/source/v9.4.5/postgresql-%{realversion}.tar.gz
Requires: openssl

%prep
%setup -n postgresql-%{realversion}

%build
export CFLAGS="-I${OPENSSL_ROOT}/include"
export LDFLAGS="-L${OPENSSL_ROOT}/lib"
./configure --prefix=%{i} --disable-static --with-openssl --without-readline

#Build libpq
cd src/interfaces/libpq/
make %{makeprocesses}

#Build pg_config
cd ../../bin/pg_config/
make %{makeprocesses}

%install
#Install libpq
cd src/interfaces/libpq/
make install

#Install pg_config
cd ../../bin/pg_config/
make install

#Copy required includes
cd ../../include/
cp postgres_ext.h %{i}/include/
cp pg_config_ext.h %{i}/include/
mkdir %{i}/include/libpq
cp libpq/libpq-fs.h %{i}/include/libpq/
