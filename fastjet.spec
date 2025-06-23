### RPM external fastjet 3.1.0
%define tag 5e4e8ed7a6ebcca0467add9d1a22d2f7cf6cdbd3
%define branch cms/v%{realversion}
%define github_user cms-externals
Source: git+https://github.com/%{github_user}/fastjet.git?obj=%{branch}/%{tag}&export=%{n}-%{realversion}&output=/%{n}-%{realversion}.tgz

%prep
%setup -n %{n}-%{realversion}

# Update to detect aarch64 and ppc64le
rm -f ./config.{sub,guess} ./plugins/SISCone/siscone/config.{sub,guess}
%get_config_sub ./config.sub
%get_config_guess ./config.guess
chmod +x ./config.{sub,guess}

cp ./config.sub   ./plugins/SISCone/siscone/config.sub
cp ./config.guess ./plugins/SISCone/siscone/config.guess

CXXFLAGS="-O3 -Wall -ffast-math -ftree-vectorize"

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
