### RPM external fastjet 3.0.3
Source: http://www.lpthe.jussieu.fr/~salam/fastjet/repo/%n-%realversion.tar.gz
Patch1: fastjet-3.0.3-nobanner
Patch2: fastjet-3.0.1-siscone-banner
Patch3: fastjet-3.0.1-noemptyareawarning
Patch4: fastjet-3.0.1-nodegeneracywarning
Patch5: fastjet-3.0.1-cluster-sequence-banner
Patch6: fastjet-3.0.1-silence-warnings

%prep
%setup -n %n-%realversion
%patch1 -p1
%patch2 -p1
%patch3 -p1
%patch4 -p1
%patch5 -p1
%patch6 -p1

case %cmsplatf in
    *_gcc4[01234]*) ;;
    *) CXXFLAGS="-O3 -Wall -ffast-math -std=c++0x -msse3 -ftree-vectorize" ;;
esac


./configure --enable-shared  --enable-atlascone --enable-cmsiterativecone --enable-siscone --prefix=%i --enable-allcxxplugins ${CXXFLAGS+CXXFLAGS="$CXXFLAGS"}

%build
make %makeprocesses

%install
make install
rm -rf %i/lib/*.la
%post
%{relocateConfig}bin/fastjet-config
