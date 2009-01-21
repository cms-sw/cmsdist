### RPM external libjpg 6b
Source: ftp://ftp.uu.net/graphics/jpeg/jpegsrc.v%{v}.tar.gz
Source1: config.sub-amd64
%prep
%setup -n jpeg-%v
%build
# libjpg ships with an old version of config.sub. 
if [ "$(uname -m)" == "x86_64" ]
then
cp %{_sourcedir}/config.sub-amd64 config.sub
fi
./configure --prefix=%{i} --enable-shared --enable-static

make %makeprocesses
%install
mkdir -p %{i}/lib
mkdir -p %{i}/bin
mkdir -p %{i}/include
mkdir -p %{i}/man/man1
make install
