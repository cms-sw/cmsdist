### RPM external fastjet 3.4.1
## INITENV +PATH PYTHON3PATH %{i}/${PYTHON3_LIB_SITE_PACKAGES}
## INCLUDE compilation_flags

BuildRequires: autotools
Requires: python3
%define tag e843c303828cd0b882d386decc35ad8c1b19df3d
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

%ifarch x86_64
CXXFLAGS="${CXXFLAGS} -msse3"
%endif
%if "%{?arch_build_flags}"
CXXFLAGS="${CXXFLAGS} %{arch_build_flags}"
%endif

PYTHON=$(which python3) \
  ./configure \
  --enable-shared \
  --enable-atlascone \
  --enable-cmsiterativecone \
  --enable-siscone \
  --prefix=%{i} \
  --enable-allcxxplugins \
  --enable-pyext \
  --enable-limited-thread-safety \
  CXXFLAGS="$CXXFLAGS"

%build
make %{makeprocesses}

%install
make install
rm -rf %{i}/lib/*.la

%post
%{relocateConfig}bin/fastjet-config
%relocateConfigAll lib _fastjet.la
