### RPM external clarens-runtime-tool 1

# DO NOT EDIT!
# This file was automatically generated using initenv
#



# Dependencies
Requires: zlib
Requires: openssl
Requires: python
Requires: libjio
Requires: tdb
Requires: python-tdb
Requires: py2-json
Requires: clarens-avl
Requires: py-xmlrpc
Requires: m2crypto
Requires: apache
Requires: mod_python
Requires: py2-monalisa-apmon
Requires: gridsite

Source: none

%prep
pwd
mkdir -p %n-%v

%build
%install


mkdir -p %i/etc/profile.d
cat << DEPS_SETUP > %i/etc/profile.d/dependencies-setup.sh
#!/bin/sh

EXTERNAL_ROOT=\$CLARENS_RUNTIME_TOOL_ROOT"/../.."

source \$EXTERNAL_ROOT/zlib/1.1.4/etc/profile.d/init.sh
source \$EXTERNAL_ROOT/openssl/0.9.7d/etc/profile.d/init.sh
source \$EXTERNAL_ROOT/python/2.4.3/etc/profile.d/init.sh
source \$EXTERNAL_ROOT/libjio/0.22/etc/profile.d/init.sh
source \$EXTERNAL_ROOT/tdb/1.0.6/etc/profile.d/init.sh
source \$EXTERNAL_ROOT/python-tdb/0.0.6/etc/profile.d/init.sh
source \$EXTERNAL_ROOT/py2-json/0.1/etc/profile.d/init.sh
source \$EXTERNAL_ROOT/clarens-avl/0.3.4/etc/profile.d/init.sh
source \$EXTERNAL_ROOT/py-xmlrpc/0.8.8.2/etc/profile.d/init.sh
source \$EXTERNAL_ROOT/m2crypto/0.15/etc/profile.d/init.sh
source \$EXTERNAL_ROOT/apache/2.0.59/etc/profile.d/init.sh
source \$EXTERNAL_ROOT/mod_python/3.2.8/etc/profile.d/init.sh
source \$EXTERNAL_ROOT/py2-monalisa-apmon/2.2.1/etc/profile.d/init.sh
source \$EXTERNAL_ROOT/gridsite/1.0.0/etc/profile.d/init.sh

DEPS_SETUP

