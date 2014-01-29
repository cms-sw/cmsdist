### RPM external qmtest 2.3.0
Requires: python
%define downloadv %(echo %v | cut -d. -f 1,2)
Source: http://www.codesourcery.com/public/qmtest/qm-%{downloadv}/qm-%{downloadv}.tar.gz

%prep
%setup -n qm-%{downloadv}

%build
python setup.py build  

%install
python setup.py install --prefix=%i 
perl -p -i -e "s|^#!.*python|/usr/bin/env python|" %{i}/bin/qmtest %{i}/bin/qmtest.py
# %test
# make check
