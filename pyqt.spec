### RPM external pyqt 4.11.4
## INITENV +PATH PYTHON27PATH %i/lib/python`echo $PYTHON_VERSION | cut -d. -f 1,2`/site-packages
%define tag 2d7924145efbdb1eafa9032646d828088c5950d5
%define branch cms/v%{realversion}
%define github_user cms-externals
Source: git+https://github.com/%github_user/%{n}.git?obj=%{branch}/%{tag}&export=%{n}-%{realversion}&output=/%{n}-%{realversion}.tgz
Requires: python
Requires: qt
Requires: sip

%prep
%setup -n %{n}-%{realversion}
# pyqt builds and uses an helper program "qtdirs" to determine where qt is installed.
# We had to patch its sources so that it reads the configuration file qt.conf
# like other qt applications, so that we get the correctly relocated information.
# Notice that in the build section we copy qt.conf from the QT installation to 
# get the correct location.

%build
# See above for explanation.
cp $QT_ROOT/bin/qt.conf . 
# Build with system compiler even when building with gcc 4.6.1, since thats the
# only way one can actually get the cocoa stuff to build. 
case %cmsos in
  osx*)
    export PATH=/usr/bin:$PATH
  ;;
esac

echo yes | python ./configure.py --sipdir=%{i}/share/PyQt4  --verbose -b %{i}/bin -d %{i}/lib/python`echo $PYTHON_VERSION | cut -d. -f 1,2`/site-packages \
                                 -e %i/include \
                                `find $QT_ROOT/include/ -type d | xargs -n 1 basename| grep -v include | xargs echo | sed -e 's| | --enable=|g;s|^|--enable=|'` 

make %makeprocesses

%install
make install

%post
ln -s dependencies-setup.sh $RPM_INSTALL_PREFIX/%{pkgrel}/etc/profile.d/init-standalone.sh
# bla bla
