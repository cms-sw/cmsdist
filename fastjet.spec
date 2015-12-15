### RPM external fastjet 3.1.0
%define tag 5e4e8ed7a6ebcca0467add9d1a22d2f7cf6cdbd3
%define branch cms/v%{realversion}
%define github_user cms-externals
Source: git+https://github.com/%{github_user}/fastjet.git?obj=%{branch}/%{tag}&export=%{n}-%{realversion}&output=/%{n}-%{realversion}.tgz

%prep
%setup -n %{n}-%{realversion}

# Update to detect aarch64 and ppc64le
rm -f ./config.{sub,guess}
curl -L -k -s -o ./config.sub 'http://git.savannah.gnu.org/gitweb/?p=config.git;a=blob_plain;f=config.sub;hb=HEAD'
curl -L -k -s -o ./config.guess 'http://git.savannah.gnu.org/gitweb/?p=config.git;a=blob_plain;f=config.guess;hb=HEAD'
chmod +x ./config.{sub,guess}

rm -f ./plugins/SISCone/siscone/config.{sub,guess}
curl -L -k -s -o ./plugins/SISCone/siscone/config.sub 'http://git.savannah.gnu.org/gitweb/?p=config.git;a=blob_plain;f=config.sub;hb=HEAD'
curl -L -k -s -o ./plugins/SISCone/siscone/config.guess 'http://git.savannah.gnu.org/gitweb/?p=config.git;a=blob_plain;f=config.guess;hb=HEAD'
chmod +x ./plugins/SISCone/siscone/config.{sub,guess}

CXXFLAGS="-O3 -Wall -ffast-math -std=c++11 -ftree-vectorize"

case %{cmsplatf} in
    *_amd64_*) CXXFLAGS="${CXXFLAGS} -msse3" ;;
esac

./configure \
  --enable-shared \
  --enable-atlascone \
  --enable-cmsiterativecone \
  --enable-siscone \
  --prefix=%{i} \
  --enable-allcxxplugins \
  CXXFLAGS="$CXXFLAGS"

%build
make %{makeprocesses}

%install
make install
rm -rf %{i}/lib/*.la
%post
%{relocateConfig}bin/fastjet-config
