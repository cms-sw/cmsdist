### RPM external dablooms 0.9.1
## INITENV +PATH PYTHON27PATH %i/${PYTHON_LIB_SITE_PACKAGES}

Source: https://github.com/bitly/dablooms/archive/v%realversion.tar.gz
Requires: python

%prep
%setup -n dablooms-%realversion

%build
make VERBOSE=1 all


%install
make VERBOSE=1 install prefix=%i
