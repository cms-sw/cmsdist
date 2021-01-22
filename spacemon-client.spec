### RPM cms spacemon-client 1.0.3
## NOCOMPILER
## INITENV +PATH PERL5LIB %i
## INITENV +PATH PATH %i/DMWMMON/SpaceMon/Utilities

%define downloadn %(echo %n | cut -f1 -d-)
%define downloadm DMWMMON
%define downloadt %(echo %realversion | tr '.' '_')
%define setupdir  %{downloadm}-%{n}_%{downloadt}
Source: https://github.com/dmwm/DMWMMON/archive/%{n}_%{downloadt}.tar.gz
Requires: p5-crypt-ssleay p5-test-simple

# Provided by system perl
Provides: perl(LWP::UserAgent)

%prep

%setup -n %{setupdir}
 
%build

%install
# Get all SpaceMon sources into DMWMMON, as module names expect it:
mkdir -p %i/DMWMMON
tar -c SpaceMon | tar -x -C %i/DMWMMON

# Add p5-crypt-ssleay/openssl environment required at run time
mkdir -p %i/etc/profile.d
: > %i/etc/profile.d/dependencies-setup.sh
: > %i/etc/profile.d/dependencies-setup.csh
for tool in p5-crypt-ssleay; do
  root=$(echo $tool | tr a-z- A-Z_)_ROOT; eval r=\$$root
  if [ X"$r" != X ] && [ -r "$r/etc/profile.d/init.sh" ]; then
    echo "test X\$$root != X || . $r/etc/profile.d/init.sh" >> %i/etc/profile.d/dependencies-setup.sh
    echo "test X\$?$root = X1 || source $r/etc/profile.d/init.csh" >> %i/etc/profile.d/dependencies-setup.csh
  fi
done

%post
%{relocateConfig}etc/profile.d/dependencies-setup.*sh
