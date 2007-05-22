### RPM external libjpg 6b-XXXX
Source: ftp://ftp.uu.net/graphics/jpeg/jpegsrc.v%{realversion}.tar.gz
Source1: config.sub-amd64
Patch0: libjpg-config.sub
Patch1: libjpg-config.guess
Patch2: libjpg-ltmain.sh
Patch3: libjpg-ltconfig
Patch4: libjpg-makefile.cfg
%prep
%setup -n jpeg-%realversion
%patch0
%patch1
%patch2
%patch3
%patch4


%build
# libjpg ships with an old version of config.sub. 
if [ "$(uname -m)" == "x86_64" ] || [ "$(uname -m)" == "ppc64" ]
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
%post
%{relocateConfig}lib/libjpeg.la
