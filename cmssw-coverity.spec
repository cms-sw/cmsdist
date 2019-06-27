### RPM cms cmssw-coverity 1.0
Requires: cmssw SCRAMV1
Source: none

%define scram        $SCRAMV1_ROOT/bin/scram --arch %cmsplatf

# Use coverity to analyse CMSSW.
# 
# * Must be run on lxbuild146 for the moment due to licensing issues.
# * Cannot use more than -j 8 due to licensing issues.
# * Must have a file ~/.cov-passwd holding the password for the admin
#   user of the Coverity Integration Manager. This means that cmsBuild
#   must be started with a valid /afs token. Token can expire once
#   the password is retrieved below.

%prep
# Prepare the area only if not already there.
# However do sscram b clean at top level in order to guarantee
# we are fine. Use rsync to minimize the source copies.
%scram project CMSSW $CMSSW_VERSION
cd $CMSSW_VERSION
%scram b clean
eval `%scram run -sh`
rsync -av $CMSSW_RELEASE_BASE/src/ src/

%build
PASSWD=`cat ~/.cov-passwd`
STREAM=`echo $CMSSW_VERSION | cut -f1,2,3 -d_`_X
cd $CMSSW_VERSION
eval `%scram run -sh`
COVERITY_ROOT=/build/coverity/5.5.1/Static-Analysis
$COVERITY_ROOT/bin/cov-configure --compiler c++ --comptype g++ --config %i/cfg/coverity_configure.xml
$COVERITY_ROOT/bin/cov-build --config %i/cfg/coverity_configure.xml --dir %i/intermediate-dir scram build %makeprocesses
CHK=`$COVERITY_ROOT/bin/cov-analyze --list-checkers | grep -v 'Available ' | grep -v symbian | grep -v -E '^COM\.' | grep -v -E '^MISRA_CAST ' | grep -v -E '^USER_POINTER '  | grep -v -E '^INTEGER_OVERFLOW ' | grep -v -E '^STACK_USE ' | sed 's, (.*$,,' | sed -e 's/^/-en /g' | xargs echo`
$COVERITY_ROOT/bin/cov-analyze ${MODELS+--user-model-file $MODELS} --disable-default --dir %i/intermediate-dir -j 8 -en $CHK
echo $COVERITY_ROOT/bin/cov-commit-defects --host 127.0.0.1 --dataport 9090 --user admin --password $PASSWD --stream $STREAM --strip-path $PWD/src --strip-path %instroot --dir %i/intermediate-dir > %i/bin/commit-coverity-defects
chmod +x %i/bin/commit-coverity-defects
%i/bin/commit-coverity-defects
%install
%post
%{relocateConfig}bin/commit-coverity-defects
# bla bla
