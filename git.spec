### RPM external git 1.8.3.1

%define isDarwin %(case %{cmsos} in (osx*) echo 1 ;; (*) echo 0 ;; esac)

Source: https://github.com/git/git/archive/v%{realversion}.tar.gz

Requires: curl expat openssl zlib pcre

%prep
%setup -n %{n}-%{realversion}

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
     NO_PERL=1 \
     V=1 \
     %{makeprocesses} \
     all

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
     NO_PERL=1 \
     V=1 \
     %{makeprocesses} \
     install

%post
%{relocateConfig}libexec/git-core/git-sh-i18n
%{relocateConfig}libexec/git-core/git-citool
%{relocateConfig}libexec/git-core/git-gui
