### RPM external git 2.23.0
## INITENV +PATH PATH %{i}/bin
## INITENV +PATH PATH %{i}/libexec/git-core
## INITENV SET GIT_TEMPLATE_DIR %{i}/share/git-core/templates
## INITENV SET GIT_SSL_CAINFO %{i}/share/ssl/certs/ca-bundle.crt
## INITENV SET GIT_EXEC_PATH %{i}/libexec/git-core

Source0: https://github.com/git/git/archive/v%{realversion}.tar.gz
Source1: https://raw.github.com/bagder/curl/curl-7_59_0/lib/mk-ca-bundle.pl
Patch1: git-2.19.0-runtime

Requires: curl expat zlib pcre2
BuildRequires: autotools
Provides: perl(SVN::Core)
Provides: perl(SVN::Delta)
Provides: perl(SVN::Ra)

%define drop_files %{i}/share/man

%prep
%setup -b 0 -n %{n}-%{realversion}
%patch1 -p1

%build
export LDFLAGS=""
export NO_LIBPCRE1_JIT=1
make %{makeprocesses} configure
./configure prefix=%{i} \
   --with-curl=${CURL_ROOT} \
   --with-expat=${EXPAT_ROOT} \
   --with-libpcre=${PCRE2_ROOT} \
   --without-python \
   --with-zlib=${ZLIB_ROOT}
   
make %{makeprocesses} \
  NO_GETTEXT=1 \
  NO_R_TO_GCC_LINKER=1 \
  RUNTIME_PREFIX=1 \
  V=1 \
  NO_CROSS_DIRECTORY_HARDLINK=1 \
  NO_INSTALL_HARDLINKS=1 \
  all

# Generate ca-bundle.crt (Certification Authority certificates)
mkdir ./ca-bundle
pushd ./ca-bundle
cp %{SOURCE1} ./mk-ca-bundle.pl
chmod +x ./mk-ca-bundle.pl
./mk-ca-bundle.pl
popd

%install
export NO_LIBPCRE1_JIT=1
make %{makeprocesses} \
  V=1 \
  NO_CROSS_DIRECTORY_HARDLINK=1 \
  NO_INSTALL_HARDLINKS=1 \
  install

# Install ca-bundle.crt (Certification Authority certificates)
mkdir -p %{i}/share/ssl/certs
cp ./ca-bundle/ca-bundle.crt %{i}/share/ssl/certs/ca-bundle.crt

%post
%{relocateConfig}bin/git-cvsserver
%{relocateConfig}libexec/git-core/git-sh-i18n
%{relocateConfig}libexec/git-core/git-add--interactive
%{relocateConfig}libexec/git-core/git-archimport
%{relocateConfig}libexec/git-core/git-cvsexportcommit
%{relocateConfig}libexec/git-core/git-cvsimport
%{relocateConfig}libexec/git-core/git-cvsserver
%{relocateConfig}libexec/git-core/git-instaweb
%{relocateConfig}libexec/git-core/git-send-email
%{relocateConfig}libexec/git-core/git-svn
%{relocateConfig}libexec/git-core/git-citool
%{relocateConfig}libexec/git-core/git-gui
%{relocateConfig}share/perl5/Git/I18N.pm
%{relocateConfig}share/gitweb/gitweb.cgi
%{relocateConfig}lib64/perl5/auto/Git/.packlist
