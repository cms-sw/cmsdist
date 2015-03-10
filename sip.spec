### RPM external sip 4.11.2
## INITENV +PATH PYTHONPATH %i/lib/python$(echo $PYTHON_VERSION |cut -d. -f 1,2)/site-packages
%define tag 51f6c53b52d0330ba46ecfd772a0a03db18ec75f
%define branch cms/v%{realversion}
%define github_user cms-externals
Source: git+https://github.com/%github_user/%{n}.git?obj=%{branch}/%{tag}&export=%{n}-%{realversion}&output=/%{n}-%{realversion}.tgz
Requires: python

%prep
%setup -n %{n}-%{realversion}

%build
python ./configure.py -v %i/share -b %i/bin -d %i/lib/python`echo $PYTHON_VERSION | cut -d. -f 1,2`/site-packages -e %i/include
make %makeprocesses

%install
make install

%post
%{relocateConfig}lib/python2.7/site-packages/sipconfig.py
