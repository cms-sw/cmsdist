### RPM external git 2.54.0
## INITENV +PATH PATH %{i}/bin
## INITENV +PATH PATH %{i}/libexec/git-core
## INITENV SET GIT_TEMPLATE_DIR %{i}/share/git-core/templates
## INITENV SET GIT_EXEC_PATH %{i}/libexec/git-core

Source0: https://github.com/git/git/archive/v%{realversion}.tar.gz
Patch1: git-2.19.0-runtime

Requires: curl expat zlib pcre2 python3
BuildRequires: autotools

%define drop_files %{i}/share/man
%define runpath_opts -m libexec

%prep
%setup -b 0 -n %{n}-%{realversion}
%patch1 -p1
sed -i -e 's|$(sysconfdir)/git|etc/git|' Makefile

%build
export LDFLAGS=""
export NO_LIBPCRE1_JIT=1
make %{makeprocesses} configure
./configure prefix=%{i} \
   --with-curl=${CURL_ROOT} \
   --with-expat=${EXPAT_ROOT} \
   --with-libpcre=${PCRE2_ROOT} \
   --with-python=$(which python3) \
   --with-zlib=${ZLIB_ROOT}
   
make %{makeprocesses} \
  NO_GETTEXT=1 \
  NO_R_TO_GCC_LINKER=1 \
  RUNTIME_PREFIX=1 \
  V=1 \
  NO_CROSS_DIRECTORY_HARDLINK=1 \
  NO_INSTALL_HARDLINKS=1 \
  all

%install
export NO_LIBPCRE1_JIT=1
make %{makeprocesses} \
  V=1 \
  NO_CROSS_DIRECTORY_HARDLINK=1 \
  NO_INSTALL_HARDLINKS=1 \
  install

perl -p -i -e "s|^#!.*python.*|#!/usr/bin/env python3|" %{i}/libexec/git-core/git-p4

%post
%{relocateConfig}bin/git-cvsserver
%{relocateConfig}libexec/git-core/git-sh-i18n
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
