### RPM external fastjet 2.4.0
Source: http://www.lpthe.jussieu.fr/~salam/fastjet/repo/%n-%realversion.tar.gz
Patch1: fastjet-2.1.0-nobanner
Patch2: fastjet-2.3.4-siscone-banner
Patch3: fastjet-2.4.0-gcc44

%prep
%setup -n %n-%realversion
%patch1 -p1
%patch2 -p1
%patch3 -p1

./configure --enable-shared --enable-cmsiterativecone --enable-atlascone --prefix=%i

%build
make

%install
make install
