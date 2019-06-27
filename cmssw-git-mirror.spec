### RPM cms cmssw-git-mirror 1.0.0
BuildRequires: cmssw
Source: none
%define initenv	        %initenv_direct
#%define name1 1937
#%define moduleName LogParser
#%define url HTMLFiles/
#Source: svn://svn.cern.ch/reps/CMSIntBld/tags/LogParser/parser?scheme=svn+ssh&revision=%{name1}&module=%{moduleName}&output=/%{moduleName}.tar.gz

%prep
%build
git clone https://:@git.cern.ch/kerberos/CMSSW src
cd src
BRANCH=`echo $CMSSW_VERSION | sed -e 's/_X.*/_X/`
git checkout $BRANCH
rsync -av --exclude .git --exclude "*.pyc" --delete $CMSSW_ROOT/src/ ./
git add --all .
git commit -m "$CMSSW_VERSION"
git tag "$CMSSW_VERSION"
git push -f origin $BRANCH
cd ..
rm -rf src
%install
# NOP

%post
# NOP
# bla bla
