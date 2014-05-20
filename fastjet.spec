### RPM external fastjet 3.0.3
%define mic %(case %cmsplatf in (*_mic_*) echo true;; (*) echo false;; esac)
%if "%mic" == "true"
Requires: icc
%endif
Source: http://www.lpthe.jussieu.fr/~salam/fastjet/repo/%n-%realversion.tar.gz
Patch1: fastjet-3.0.3-nobanner
Patch2: fastjet-3.0.1-siscone-banner
Patch3: fastjet-3.0.1-noemptyareawarning
Patch4: fastjet-3.0.1-nodegeneracywarning
Patch5: fastjet-3.0.1-cluster-sequence-banner
Patch6: fastjet-3.0.1-silence-warnings

%prep
%setup -n %n-%realversion

case %cmsplatf in
    *_gcc4[01234]* ) ;;
    *_armv7hl_* ) CXXFLAGS="-O3 -Wall -ffast-math -std=c++0x -ftree-vectorize" ;;
    *_mic_* ) CXXFLAGS="-O3 -Wall -ffast-math -std=c++0x -ftree-vectorize" ;;
    * ) CXXFLAGS="-O3 -Wall -ffast-math -std=c++0x -msse3 -ftree-vectorize" ;;
esac


case %{cmsplatf} in
   *_mic_* )
    CXX="icpc -fPIC -mmic"  CC="icc -fPIC -mmic" ./configure --enable-shared  --enable-atlascone --enable-cmsiterativecone --enable-siscone --prefix=%i --enable-allcxxplugins ${CXXFLAGS+CXXFLAGS="$CXXFLAGS"} --host=x86_64-k1om-linux
     ;;
   * )
     ./configure --enable-shared  --enable-atlascone --enable-cmsiterativecone --enable-siscone --prefix=%i --enable-allcxxplugins ${CXXFLAGS+CXXFLAGS="$CXXFLAGS"}
     ;;
esac

%build
make %makeprocesses

%install
make install
rm -rf %i/lib/*.la
%post
%{relocateConfig}bin/fastjet-config
