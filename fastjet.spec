### RPM external fastjet 3.0.3
%define tag 87f4ff1f4a606ed82ca4f07d02bc0bce190ceeaf
%define branch cms/v%realversion
%define github_user cms-externals
Source: git+https://github.com/%github_user/fastjet.git?obj=%{branch}/%{tag}&export=%{n}-%{realversion}&output=/%{n}-%{realversion}.tgz
%define mic %(case %cmsplatf in (*_mic_*) echo true;; (*) echo false;; esac)
%if "%mic" == "true"
Requires: icc
%endif

%prep
%setup -n %n-%realversion

case %cmsplatf in
    *_gcc4[01234]* ) ;;
    *_armv7hl_* ) CXXFLAGS="-O3 -Wall -ffast-math -std=c++0x -ftree-vectorize" ;;
    *_mic_* ) CXXFLAGS="-O3 -Wall -ffast-math -std=c++0x -ftree-vectorize -Dthread_local=" ;;
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
