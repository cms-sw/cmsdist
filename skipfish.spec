### RPM external skipfish 2.10b
Source: http://skipfish.googlecode.com/files/%n-%realversion.tgz
Requires: pcre libidn

%prep
%setup -q -n %n-%{realversion}

%build
export CFLAGS="-I${PCRE_ROOT}/include -I${LIBIDN_ROOT}/include"
export LDFLAGS="-L${PCRE_ROOT}/lib -L${LIBIDN_ROOT}/lib"
make %{makeprocesses}

%install
mkdir %i/bin
cp skipfish %i/bin
cp -rp assets dictionaries signatures %i/
