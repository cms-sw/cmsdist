### RPM external clarens-build-tool 1

# DO NOT EDIT!
# This file was automatically generated using initenv
#



# Dependencies
Requires: gcc
Requires: swig
Requires: python
Requires: pyrex
Requires: zlib
Requires: openssl
Requires: libjio
Requires: tdb

Source: none

%prep
pwd
mkdir -p %n-%v

%build
%install


mkdir -p %i/etc/profile.d
cat << DEPS_SETUP > %i/etc/profile.d/dependencies-setup.sh
#!/bin/sh

EXTERNAL_ROOT=\$CLARENS_BUILD_TOOL_ROOT"/../.."

source \$EXTERNAL_ROOT/gcc/3.2.3/etc/profile.d/init.sh
source \$EXTERNAL_ROOT/swig/1.3.29/etc/profile.d/init.sh
source \$EXTERNAL_ROOT/python/2.4.3/etc/profile.d/init.sh
source \$EXTERNAL_ROOT/pyrex/0.9.3.1/etc/profile.d/init.sh
source \$EXTERNAL_ROOT/zlib/1.1.4/etc/profile.d/init.sh
source \$EXTERNAL_ROOT/openssl/0.9.7d/etc/profile.d/init.sh
source \$EXTERNAL_ROOT/libjio/0.22/etc/profile.d/init.sh
source \$EXTERNAL_ROOT/tdb/1.0.6/etc/profile.d/init.sh

DEPS_SETUP

