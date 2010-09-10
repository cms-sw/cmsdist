### RPM external mod_wsgi 3.3
## INITENV +PATH PYTHONPATH %i/lib/python`echo $PYTHON_VERSION | cut -d. -f 1,2`/site-packages
Source0: http://modwsgi.googlecode.com/files/%n-%realversion.tar.gz
Requires: apache2 python

%prep
%setup -n %n-%realversion

%build
./configure --prefix=%i
make %makeprocesses

%install
mkdir -p %i/modules
make %makeprocesses install LIBEXECDIR=%i/modules

# Generates dependencies-setup.{sh,csh} so init.{sh,csh} pick full environment.
mkdir -p %i/etc/profile.d
for tool in $(echo %{requiredtools} | sed -e's|\s+| |;s|^\s+||'); do
  eval "r=\$$(echo $tool | tr a-z- A-Z_)_ROOT"
  if [ X"$r" != X ] && [ -r "$r/etc/profile.d/init.sh" ]; then
    echo ". $r/etc/profile.d/init.sh" >> %{i}/etc/profile.d/dependencies-setup.sh
    echo "source $r/etc/profile.d/init.csh" >> %{i}/etc/profile.d/dependencies-setup.csh
  fi
done

%post
%{relocateConfig}etc/profile.d/dependencies-setup.*sh
