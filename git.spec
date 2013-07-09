### RPM external git 1.8.3.1

%define isDarwin %(case %{cmsos} in (osx*) echo 1 ;; (*) echo 0 ;; esac)

%define curl_tag curl-7_31_0

Source0: https://github.com/git/git/archive/v%{realversion}.tar.gz
Patch1: git-1.8.3.1-no-symlink

Source1: https://raw.github.com/bagder/curl/%{curl_tag}/lib/mk-ca-bundle.pl

Requires: curl expat openssl zlib pcre

# Fake provides for git add --interactive
# The following are not avaialble on SLC and Darwin platforms by default
Provides: perl(DBI)
Provides: perl(Error)
Provides: perl(SVN::Client)
Provides: perl(SVN::Core)
Provides: perl(SVN::Delta)
Provides: perl(SVN::Ra)
Provides: perl(YAML::Any)

%prep
%setup -b 0 -n %{n}-%{realversion}
%patch1 -p1

%build
make prefix=%{i} \
%if %isDarwin
     NO_DARWIN_PORTS=1 \
     NO_FINK=1 \
%endif
     CURLDIR="${CURL_ROOT}" \
     OPENSSLDIR="${OPENSSL_ROOT}" \
     EXPATDIR="${EXPAT_ROOT}" \
     ZLIB_PATH="${ZLIB_ROOT}" \
     USE_LIBPCRE=1 \
     NO_GETTEXT=1 \
     NO_R_TO_GCC_LINKER=1 \
     LIBPCREDIR="${PCRE_ROOT}" \
     NO_PYTHON=1 \
     V=1 \
     %{makeprocesses} \
     all

# Generate ca-bundle.crt (Certification Authority certificates)
mkdir ./ca-bundle
pushd ./ca-bundle
cp %{SOURCE1} ./mk-ca-bundle.pl
chmod +x ./mk-ca-bundle.pl
./mk-ca-bundle.pl
popd

%install
make prefix=%{i} \
%if %isDarwin
     NO_DARWIN_PORTS=1 \
     NO_FINK=1 \
%endif
     CURLDIR="${CURL_ROOT}" \
     OPENSSLDIR="${OPENSSL_ROOT}" \
     EXPATDIR="${EXPAT_ROOT}" \
     ZLIB_PATH="${ZLIB_ROOT}" \
     USE_LIBPCRE=1 \
     NO_GETTEXT=1 \
     NO_R_TO_GCC_LINKER=1 \
     LIBPCREDIR="${PCRE_ROOT}" \
     NO_PYTHON=1 \
     V=1 \
     %{makeprocesses} \
     install

# Install ca-bundle.crt (Certification Authority certificates)
mkdir -p %{i}/share/ssl/certs
cp ./ca-bundle/ca-bundle.crt %{i}/share/ssl/certs/ca-bundle.crt

%post
%{relocateConfig}libexec/git-core/git-sh-i18n
%{relocateConfig}libexec/git-core/git-citool
%{relocateConfig}libexec/git-core/git-gui
