### RPM external rats 2.4
Source: https://rough-auditing-tool-for-security.googlecode.com/files/%n-%realversion.tgz
Requires: expat

%prep
%setup -q -n %n-%{realversion}

%build
./configure --prefix=%i --with-expat-lib=${EXPAT_ROOT}/lib --with-expat-include=${EXPAT_ROOT}/include
make %{makeprocesses}

%install
make install
%define drop_files %i/{man,lib}
