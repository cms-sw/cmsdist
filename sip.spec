### RPM external sip 4.17
## INITENV +PATH PYTHON27PATH %i/lib/python$(echo $PYTHON_VERSION |cut -d. -f 1,2)/site-packages
%define tag f5f49b1c14cd058c2736ade2fef0abb0765b8be4
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
# bla bla
