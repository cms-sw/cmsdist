### RPM external py2-mysqldb 1.2.3c1
%define pythonv `echo $PYTHON_VERSION | cut -d. -f 1,2`
## INITENV +PATH PYTHONPATH %i/lib/python%{pythonv}/site-packages
%define downloadn MySQL-python
Source: http://heanet.dl.sourceforge.net/sourceforge/mysql-python/%downloadn-%realversion.tar.gz
Requires: python mysql 
Patch0: py2-mysqldb-setup
%prep
%setup -n %downloadn-%realversion
%patch0 -p0
%build
python setup.py build
%install
python setup.py install --prefix=%{i}

# Dependencies
rm -rf %i/etc/profile.d
mkdir -p %i/etc/profile.d
for x in %pkgreqs; do
  case $x in /* ) continue ;; esac
  p=%{instroot}/%{cmsplatf}/$(echo $x | sed 's/\([^+]*\)+\(.*\)+\([A-Z0-9].*\)/\1 \2 \3/' | tr ' ' '/')
  echo ". $p/etc/profile.d/init.sh" >> %i/etc/profile.d/dependencies-setup.sh
  echo "source $p/etc/profile.d/init.csh" >> %i/etc/profile.d/dependencies-setup.csh
done

%post
# The relocation below is also needed in case of dependencies
%{relocateConfig}etc/profile.d/dependencies-setup.sh
%{relocateConfig}etc/profile.d/dependencies-setup.csh

