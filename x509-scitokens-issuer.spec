### RPM external x509-scitokens-issuer v0.6.2
## INITENV +PATH PYTHONPATH %i/${PYTHON_LIB_SITE_PACKAGES}
Source0: git://github.com/scitokens/x509-scitokens-issuer.git?obj=master/%{realversion}&export=%n&output=/%n.tar.gz
Requires: python py2-setuptools py2-requests py2-scitokens py2-flask py2-gunicorn py2-cryptography

%prep
%setup -b 0 -n %n

%build

%install
mkdir -p %i/$PYTHON_LIB_SITE_PACKAGES

# NOTE: we can't use standard install since it writes data in system areas
#PYTHONPATH=%i/$PYTHON_LIB_SITE_PACKAGES:$PYTHONPATH \
#python setup.py install --prefix=%i

cp -r src/x509_scitokens_issuer %i/$PYTHON_LIB_SITE_PACKAGES
cp -r wsgi configs %i
mkdir %i/bin
cp tools/{cms-scitoken-init,cms-update-mapping,x509-scitoken-init,macaroon-init} %i/bin

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
