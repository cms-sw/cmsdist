### RPM external pacman 2.129
## INITENV +PATH PYTHONPATH %i/src
## INITENV SET PACMAN_LOCATION %i
#FIXME: always gets the latest version...
Source: http://physics.bu.edu/pacman/sample_cache/tarballs/%n-%v.tar.gz
Requires: python
%prep
%setup -n %n-%v
%build
%install
cp -r ./* %i
ln -sf %i/caches_starter %i/src/caches_starter 
