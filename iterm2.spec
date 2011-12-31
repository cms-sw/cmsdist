### RPM external iterm2 1.0

Source: git://github.com/ktf/iTerm2.git?export=iterm2-%realversion&branch=cmssw&tag=b794b1e77881a9ebeff2edb9dfa932a795562871&output=/iterm2-%realversion.tgz
Provides: Growl Sparkle

%prep
%setup -n iterm2-%realversion

%build
rm -rf build
xcodebuild clean
xcodebuild build -configuration Deployment
%install
rsync -av build/Deployment/iTerm.app/ %instroot/
cat <<\EOF >%cmsroot/bin/cms-pkg
#!/bin/sh -e
# A simple wrapper around apt-get

appdir="`dirname $0`"/..
source $appdir/$SCRAM_ARCH/apt-init.sh

syntax() 
{
  echo "Syntax:"
  echo "cms-pkg install <CMSSW version>"
  echo "cms-pkg list"
  exit 1
}

if [ X$1 = X ]
then
  echo "Not enough arguments."
  syntax
fi

case $1 in
  list)
    apt-cache search cms\\+CMSSW\\+ | sed -e's|.*cmssw[+]||;s| - .*||'
  ;;
  install)
    if [ "X$2" = X ]; then echo "install needs a CMSSW version. E.g: CMSSW_5_0_0_pre4." ; syntax ; fi 
    apt-get install "cms+cmssw+$2"
    apt-cache clear
  ;;
  --help|-help|help)
    syntax ; exit 1
  ;;
  *)
  echo "Unknown command $1"
  syntax
  ;;
esac
EOF
chmod +x %cmsroot/bin/cms-pkg
