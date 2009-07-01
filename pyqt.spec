### RPM external pyqt 4.5
## INITENV +PATH PYTHONPATH %i/lib/python2.4/site-packages
## BUILDIF case %cmsplatf in osx*) false;; *) true;; esac
Source: http://www.riverbankcomputing.co.uk/static/Downloads/PyQt4/PyQt-x11-gpl-%realversion.tar.gz
Requires: python
Requires: qt
Requires: sip

%prep
%setup -n PyQt-x11-gpl-%realversion

%build
echo yes | python ./configure.py -b %i/bin -d %i/lib/python`echo $PYTHON_VERSION | cut -d. -f 1,2`/site-packages \
                                 -e %i/include \
                                `find $QT_ROOT/include/ -type d | xargs -n 1 basename| grep -v include | xargs echo | sed -e 's| | --enable=|g;s|^|--enable=|'` 

make %makeprocesses

%install
make install

mkdir -p %i/etc/profile.d
cat << \EOF_INIT_ME > %i/etc/profile.d/init-standalone.sh
#!/bin/sh
source @GCC_ROOT@/etc/profile.d/init.sh
source @BZ2LIB_ROOT@/etc/profile.d/init.sh
source @EXPAT_ROOT@/etc/profile.d/init.sh
source @DB4_ROOT@/etc/profile.d/init.sh
source @GDBM_ROOT@/etc/profile.d/init.sh
source @ZLIB_ROOT@/etc/profile.d/init.sh
source @OPENSSL_ROOT@/etc/profile.d/init.sh
source @PYTHON_ROOT@/etc/profile.d/init.sh
source @QT_ROOT@/etc/profile.d/init.sh
source @SIP_ROOT@/etc/profile.d/init.sh
source %i/etc/profile.d/init.sh
EOF_INIT_ME

perl -p -i -e "s|\@([^@]*)\@|\$ENV{\$1}|" %i/etc/profile.d/init-standalone.sh
mkdir -p %i/etc/scram.d
cat << \EOF_TOOLFILE >%i/etc/scram.d/pyqt
<doc type=BuildSystem::ToolDoc version=1.0>
<Tool name=pyqt version=%v>
<info url="http://www.riverbankcomputing.co.uk/software/pyqt/intro"></info>
<Client>
 <Environment name=PYQT_BASE default="%i"></Environment>
</Client>
<Runtime name=PYTHONPATH value="$PYQT_BASE/lib/python2.4/site-packages" type=path>
<use name="python">
<use name="qt">
<use name="sip">
</Tool>
EOF_TOOLFILE

%post
%{relocateConfig}etc/scram.d/pyqt
%{relocateConfig}etc/profile.d/init-standalone.sh
