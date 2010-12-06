### RPM cms filemover 1.0.1.pre3
## INITENV +PATH PYTHONPATH %i/lib/python`echo $PYTHON_VERSION | cut -d. -f 1,2`/site-packages 

%define webdoc_files %i/doc/
%define svnserver svn://svn.cern.ch/reps/CMSDMWM/FileMover/tags/%{realversion}
Source: %svnserver?scheme=svn+ssh&strategy=export&module=FileMover&output=/filemover.tar.gz

Requires: python cherrypy py2-cheetah yui wmcore py2-sphinx rotatelogs

%prep
%setup -n FileMover

%build
python setup.py build

# build FileMover sphinx documentation
PYTHONPATH=$PWD/src/python:$PYTHONPATH
cd doc
cat sphinx/conf.py | sed "s,development,%{realversion},g" > sphinx/conf.py.tmp
mv sphinx/conf.py.tmp sphinx/conf.py
mkdir -p build
make html

%install
python setup.py install --prefix=%i
egrep -r -l '^#!.*python' %i | xargs perl -p -i -e 's{^#!.*python.*}{#!/usr/bin/env python}'
find %i -name '*.egg-info' -exec rm {} \;

mkdir -p %i/doc
tar --exclude '.buildinfo' -C doc/build/html -cf - . | tar -C %i/doc -xvf -

# Generate dependencies-setup.{sh,csh} so init.{sh,csh} picks full environment.
mkdir -p %i/etc/profile.d
: > %i/etc/profile.d/dependencies-setup.sh
: > %i/etc/profile.d/dependencies-setup.csh
for tool in $(echo %{requiredtools} | sed -e's|\s+| |;s|^\s+||'); do
  root=$(echo $tool | tr a-z- A-Z_)_ROOT; eval r=\$$root
  if [ X"$r" != X ] && [ -r "$r/etc/profile.d/init.sh" ]; then
    echo "test X\$$root != X || . $r/etc/profile.d/init.sh" >> %i/etc/profile.d/dependencies-setup.sh
    echo "test X\$$root != X || source $r/etc/profile.d/init.csh" >> %i/etc/profile.d/dependencies-setup.csh
  fi
done

%post
%{relocateConfig}etc/profile.d/dependencies-setup.*sh

%files
%i/
%exclude %i/doc


## SUBPACKAGE webdoc
