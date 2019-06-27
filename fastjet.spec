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
rm -f ./config.{sub,guess}
curl -L -k -s -o ./config.sub 'http://git.savannah.gnu.org/gitweb/?p=config.git;a=blob_plain;f=config.sub;hb=HEAD'
curl -L -k -s -o ./config.guess 'http://git.savannah.gnu.org/gitweb/?p=config.git;a=blob_plain;f=config.guess;hb=HEAD'
chmod +x ./config.{sub,guess}

rm -f ./plugins/SISCone/siscone/config.{sub,guess}
curl -L -k -s -o ./plugins/SISCone/siscone/config.sub 'http://git.savannah.gnu.org/gitweb/?p=config.git;a=blob_plain;f=config.sub;hb=HEAD'
curl -L -k -s -o ./plugins/SISCone/siscone/config.guess 'http://git.savannah.gnu.org/gitweb/?p=config.git;a=blob_plain;f=config.guess;hb=HEAD'
chmod +x ./plugins/SISCone/siscone/config.{sub,guess}

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
# bla bla
