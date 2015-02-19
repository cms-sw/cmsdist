### RPM external py2-zmq 2.1.9
## INITENV +PATH PYTHONPATH %i/lib/python`echo $PYTHON_VERSION | cut -f1,2 -d.`/site-packages

Source: https://github.com/downloads/zeromq/pyzmq/pyzmq-%realversion.tar.gz

Requires: python zeromq

%prep
%setup -n pyzmq-%realversion

# Need to tell it where zmq is for the build
# configure command for 2.1 and above
#python setup.py configure --zmq=$ZEROMQ_ROOT
# for 2.0 do manually
cp setup.cfg.template setup.cfg
perl -p -i -e 's!/usr/local!'"${ZEROMQ_ROOT}"'!g' setup.cfg

%build
python setup.py build

%install
python setup.py install --prefix=%i
find %i -name '*.egg-info' -exec rm {} \;
find %i -name '.package-checksum' -exec rm {} \;

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
%{relocateConfig}etc/profile.d/dependencies-setup.*sh

