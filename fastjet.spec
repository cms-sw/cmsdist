### RPM external fastjet 2.4.4
Source: http://www.lpthe.jussieu.fr/~salam/fastjet/repo/%n-%realversion.tar.gz
Patch1: fastjet-2.1.0-nobanner
Patch2: fastjet-2.3.4-siscone-banner
Patch3: fastjet-2.4.4-noemptyareawarning
Patch4: fastjet-2.4.4-nodegeneracywarning
Patch5: fastjet-2.4.4-fix-gcc47

%prep
%setup -n %n-%realversion
%patch1 -p1
%patch2 -p1
%patch3 -p0
%patch4 -p0
%patch5 -p1

case %cmsplatf in
    *_gcc4[01234]*) ;;
    *) CXXFLAGS="-O3 -Wall -ffast-math -std=c++0x -msse3 -ftree-vectorize" ;;
esac

./configure --enable-shared --enable-cmsiterativecone --enable-atlascone --prefix=%i --enable-allcxxplugins ${CXXFLAGS+CXXFLAGS="$CXXFLAGS"}

%build
make %makeprocesses

%install
make install
rm -rf %i/lib/*.la
