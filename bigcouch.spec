### RPM external bigcouch 0.4.2b
Source0: https://github.com/cloudant/bigcouch/archive/bigcouch-%realversion.zip
Source1: bigcouch_cms_auth.erl
Patch0: bigcouch-fix-sconscript
Patch1: bigcouch-add-cmsauth-to-chttpd
Patch2: bigcouch-megapatch
Patch3: bigcouch-ssl-replication

# Although there is no technical software dependency,
# couchapp was included because all CMS applications will need it.
# Alan on 30/Aug/2019: comment out these 2 lines below to avoid building
# bigcouch, we don't use it anyways...
#Requires: curl spidermonkey openssl icu4c erlang couchapp python
#BuildRequires: autotools gcc scons

%prep
%setup -n bigcouch-bigcouch-%realversion
%patch0 -p0
%patch3 -p0
%patch2 -p0
ls -lah %{_sourcedir}
cp %{_sourcedir}/bigcouch-add-cmsauth-to-chttpd .
cp %{_sourcedir}/bigcouch_cms_auth.erl .

%build
export CURL_ROOT SPIDERMONKEY_ROOT OPENSSL_ROOT ICU4C_ROOT ERLANG_ROOT PYTHON_ROOT

# this git-wrapper stuff is a dumb hack till zlib is fixed
mkdir -p git-wrapper
echo "#!/bin/bash" > git-wrapper/git
echo "unset LD_LIBRARY_PATH" > git-wrapper/git
echo "/usr/bin/git \$@ 2>&1 | tee -a ~/git.log" >> git-wrapper/git
echo "exit ${PIPESTATUS[0]}" >> git-wrapper/git
chmod +x git-wrapper/git
export PATH=`pwd`/git-wrapper:$PATH

sed -i 's#./rebar#./rebar verbose=1#g' configure
git clone -n https://github.com/cloudant/erlang-oauth.git oauth2
cd oauth2
git checkout -q BigCouch-0.4.0
cd ..

# bigcouch build system assumes the code is in git
cd ..
git init
touch dummy
echo "hi" >> dummy
git add dummy
# bigcouch doesn't seem to want to build from a non-git repository
git commit -m "Dummy"
git tag %realversion
cd -

./configure -p %i
# Munge configurations to point to our libraries
for CONFIG in `find . -name rebar.config`; do
if [[ $CONFIG == './apps/couch/rebar.config' ]]; then
    continue
fi
cat >> $CONFIG <<EOTT

{port_env, [
    {"DRV_CFLAGS", "\$DRV_CFLAGS -I ${ICU4C_ROOT}/include -I ${SPIDERMONKEY_ROOT}/include -I ${CURL_ROOT}/include -L ${ICU4C_ROOT}/lib -L ${SPIDERMONKEY_ROOT}/lib -L ${CURL_ROOT}/lib "},
{"LDFLAGS", " \$LDFLAGS -L ${ICU4C_ROOT}/lib -L ${SPIDERMONKEY_ROOT}/lib -L ${CURL_ROOT}/lib $LDFLAGS"},
{"DRV_LDFLAGS", "\$DRV_LDFLAGS -L ${ICU4C_ROOT}/lib -L ${SPIDERMONKEY_ROOT}/lib -L ${CURL_ROOT}/lib"},

{"DRV_CXXFLAGS", "\$DRV_CXXFLAGS -I ${ICU4C_ROOT}/include -I ${SPIDERMONKEY_ROOT}/include -I ${CURL_ROOT}/include -L ${ICU4C_ROOT}/lib -L ${SPIDERMONKEY_ROOT}/lib -L ${CURL_ROOT}/lib "},
     {"CFLAGS", "\$CFLAGS -I ${ICU4C_ROOT}/include -I ${SPIDERMONKEY_ROOT}/include -I ${CURL_ROOT}/include"}]}.
EOTT

done

# Now munge the environment to get the rest
export CFLAGS="-I ${ICU4C_ROOT}/include -I ${SPIDERMONKEY_ROOT}/include -I ${CURL_ROOT}/include -L ${ICU4C_ROOT}/lib -L ${SPIDERMONKEY_ROOT}/lib -L ${CURL_ROOT}/lib $CFLAGS"
export LDFLAGS="-L ${ICU4C_ROOT}/lib -L ${SPIDERMONKEY_ROOT}/lib -L ${CURL_ROOT}/lib $LDFLAGS"
export CXXFLAGS=" -I ${ICU4C_ROOT}/include -I ${SPIDERMONKEY_ROOT}/include -I ${CURL_ROOT}/include -L ${ICU4C_ROOT}/lib -L ${SPIDERMONKEY_ROOT}/lib -L ${CURL_ROOT}/lib $CXXFLAGS"
export CPPFLAGS=$CXXFLAGS

# Couchjs is built with scons, change those parts too
sed -i 's#@cat $(appfile) | sed s/%VSN%/`git describe --match 1.*`/ > $(appfile)#@sed -i s/%VSN%/BigCouchTarball/ $(appfile) ; cat $(appfile)#' Makefile
sed -i 's#./rebar#./rebar verbose=1#g' Makefile
sed -i "s#python scons/scons.py#python scons/scons.py spiderLib=${SPIDERMONKEY_ROOT}/lib spiderInclude=${SPIDERMONKEY_ROOT}/include curlLib=${CURL_ROOT}/lib curlInclude=${CURL_ROOT}/include#g" Makefile
sed -i 's#env = Environment(#env = Environment(ENV = os.environ, #g' couchjs/c_src/SConscript

(
# We can't patch this earlier because ./configure downloads these deps
cp bigcouch-add-cmsauth-to-chttpd deps/chttpd/src
cp bigcouch_cms_auth.erl deps/chttpd/src/couch_cms_auth.erl
cd deps/chttpd/src
patch -p1 < bigcouch-add-cmsauth-to-chttpd
)

make %makeprocesses
(
# create node for bigcouch
cd rel
../rebar create-node nodeid=bigcouch
)

%install
# still need that git wrapper because of zlib
mkdir -p git-wrapper
echo "#!/bin/bash" > git-wrapper/git
echo "unset LD_LIBRARY_PATH" > git-wrapper/git
echo "/usr/bin/git \$@ 2>&1 | tee -a ~/git.log" >> git-wrapper/git
echo "exit 0" >> git-wrapper/git
chmod +x git-wrapper/git
export PATH=`pwd`/git-wrapper:$PATH
make %makeprocesses install

# get rid of hardcoded configuration paths, we need to make things relocatable
perl -p -i -e 's,\$ROOTDIR\/etc\/vm.args,vm.args,g' %i/bin/bigcouch

# drop things we don't need or don't want on the RPM
%define drop_files %i/{man,share/doc,etc/{default,local}.ini,etc/vm.args,var}

# Generate dependencies-setup.{sh,csh} so init.{sh,csh} picks full environment.
mkdir -p %i/etc/profile.d
: > %i/etc/profile.d/dependencies-setup.sh
: > %i/etc/profile.d/dependencies-setup.csh
for tool in $(echo %{requiredtools} | sed -e's|\s+| |;s|^\s+||'); do
  root=$(echo $tool | tr a-z- A-Z_)_ROOT; eval r=\$$root
  if [ X"$r" != X ] && [ -r "$r/etc/profile.d/init.sh" ]; then
    echo "test X\$$root != X || . $r/etc/profile.d/init.sh" >> %i/etc/profile.d/dependencies-setup.sh
    echo "test X\$?$root = X1 || source $r/etc/profile.d/init.csh" >> %i/etc/profile.d/dependencies-setup.csh
  fi
done

%post
%{relocateConfig}etc/profile.d/dependencies-setup.*sh
