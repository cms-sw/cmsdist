### RPM external fastjet 3.3.0
## INITENV +PATH PYTHON27PATH %{i}/${PYTHON_LIB_SITE_PACKAGES}
Requires: python
%define tag acfff3bf99b6c754efe3768b81393935f3b9a05d
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
  --enable-pyext \
  CXXFLAGS="$CXXFLAGS"

%build
make %{makeprocesses}

%install
make install
rm -rf %{i}/lib/*.la
%post
%{relocateConfig}bin/fastjet-config
