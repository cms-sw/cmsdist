### RPM cms alertscollector 0.9.13

# private repository tests
#Source0: git://github.com/zdenekmaxa/WMCore?obj=alertscollector/HEAD&export=%n&output=/%n.tar.gz
# realversion can be taken from above, but has to correspond to a GIT tag
Source0: git://github.com/dmwm/WMCore?obj=master/%realversion&export=%n&output=/%n.tar.gz
# download tip of a branch (problem with added username and username's hash ...)
#Source0: https://github.com/zdenekmaxa/WMCore/tarball/alertscollector

# (cherrypy) bug introduced in 
# https://github.com/dmwm/WMCore/commit/2922d23d3f980caa65899f443f1a8f67a0cb8a1c
# setup_test depends on that but it's not necessary
# sphinx is also necessary for build try to produce documentation
BuildRequires: python cherrypy py2-setuptools py2-sphinx

%prep
%setup -b 0 -n %n


%build
python setup.py build_system -s alertscollector


%install
# cannot stat alertscollector directory
#cp -r alertscollector/* %i
python setup.py install_system -s alertscollector --prefix=%i
find %i -name '*.egg-info' -exec rm {} \;

# Generate dependencies-setup.{sh,csh} so init.{sh,csh} picks full environment.
# no dependencies


%post
# empty post section
