### RPM external gitweb 1.8.2.3
Requires: apache-setup apache2 mod_perl2
Source: git://git.kernel.org/pub/scm/git/git?obj=master/v%realversion&export=%n&output=/%n.tar.gz
Patch0: gitweb-do-not-guess-owner
Patch1: gitweb-fix-tab-title
BuildRequires: autotools

%prep
%setup -n %n
%patch0 -p0
%patch1 -p0

%build
make configure
./configure --prefix=%i
make gitweb

%install
make gitwebdir=%i/htdocs/gitweb install-gitweb
find %i/htdocs/gitweb -type f | xargs perl -p -i -e "s|#\!.*perl(.*)|#!/usr/bin/env perl$1|" 
perl -p -i -e 's,\$GIT = ".*?";,\$GIT = \$ENV{"SERVER_GIT"} || "git";,g' %i/htdocs/gitweb/gitweb.cgi

# Generate dependencies-setup.{sh,csh} so init.{sh,csh} picks full environment.
mkdir -p %i/etc/profile.d
: > %i/etc/profile.d/dependencies-setup.sh
: > %i/etc/profile.d/dependencies-setup.csh
for tool in $(echo %{requiredtools} | sed -e's|\s+| |;s|^\s+||'); do
  root=$(echo $tool | tr a-z- A-Z_)_ROOT; eval r=\$$root
  if [ X"$r" != X ] && [ -r "$r/etc/profile.d/init.sh" ]; then
    echo "test X\$$root != X || . $r/etc/profile.d/init.sh" >> %i/etc/profile.d/dependencies-setup.sh
    echo "test X\$?$root = X1 || source $r/etc/profile.d/init.csh" >> %i/etc/profile.d/dependencies-setup.csh
  fi
done

%post
%{relocateConfig}htdocs/gitweb/gitweb.cgi
%{relocateConfig}etc/profile.d/dependencies-setup.*sh
