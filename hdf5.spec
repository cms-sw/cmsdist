### RPM external hdf5 1.8.17
Source: https://support.hdfgroup.org/ftp/HDF5/current/src/%{n}-%{realversion}.tar.bz2
BuildRequires: zlib

%prep
%setup -n %{n}-%{realversion}

%build
rm -f ./bin/config.{sub,guess}
curl -L -k -s -o ./bin/config.sub 'http://git.savannah.gnu.org/gitweb/?p=config.git;a=blob_plain;f=config.sub;hb=HEAD'
curl -L -k -s -o ./bin/config.guess 'http://git.savannah.gnu.org/gitweb/?p=config.git;a=blob_plain;f=config.guess;hb=HEAD'
chmod +x ./bin/config.{sub,guess}
./configure --enable-shared --enable-cxx --with-zlib=${ZLIB_ROOT} --prefix %{i}
make %{makeprocesses} VERBOSE=1

%install
make install

%post
# bla bla
