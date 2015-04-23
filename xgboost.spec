### RPM external xgboost v0.32
## INITENV +PATH PYTHONPATH %i/${PYTHON_LIB_SITE_PACKAGES}

%define pkg xgboost
Source: git://github.com/tqchen/xgboost?obj=master/%realversion&export=%pkg&output=/%pkg.tar.gz

%prep
%setup -n %pkg

%build
./build.sh

%install
mkdir %i/bin
cp xgboost %i/bin
