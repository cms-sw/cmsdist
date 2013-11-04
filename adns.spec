### RPM external adns 1.4
Source: http://www.chiark.greenend.org.uk/~ian/adns/ftp/adns-%realversion.tar.gz
Patch: adns-osx-build
BuildRequires: autotools

%prep
%setup -n %n-%realversion
%ifos darwin
%patch
autoreconf -i
%endif

%build
./configure --prefix=%i
make %makeprocesses

%install
make install

%define strip_files %i/lib
