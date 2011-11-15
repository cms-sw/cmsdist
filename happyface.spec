### RPM cms happyface r656
## INITENV +PATH PYTHONPATH %i/$PYTHON_LIB_SITE_PACKAGES
%define hfrev %(echo %realversion|tr -d 'r')

Source0: http://ekphappyface.physik.uni-karlsruhe.de/~happyface/hf_svnSnapshot/hfTemplateInstance_svnSnap_%realversion.tar.bz2
Source1: svn://svn.cern.ch/reps/cmsmon/HappyFace/trunk?scheme=svn+ssh&strategy=export&module=HappyFace&output=/srcmodules.tar.gz
Requires: python py2-sqlobject py2-formencode py2-lxml py2-matplotlib

%prep
#(cd HappyFace; tar xvzf %_sourcedir/cmst1prodmon.tar.gz)
%setup -T -b 0 -n hfTemplateInstance
%setup -T -b 1 -n HappyFace

%build

%install
mkdir -p %i/$PYTHON_LIB_SITE_PACKAGES
cp -rp %_builddir/hfTemplateInstance/* %i/
mv %_builddir/HappyFace/{local,run.cfg} %i/HappyFace/
mv %i/HappyFace %i/$PYTHON_LIB_SITE_PACKAGES/
perl -p -i -e 's|matplotlib.use\("cairo.png"|#matplotlib.use\("cairo.png"|g' \
              %i/$PYTHON_LIB_SITE_PACKAGES/HappyFace/happycore/*
perl -p -i -e "s|^#!.*python|#!/usr/bin/env python|" $(find %{i} -type f)
for F in $(find %i -name '.svn'); do rm -rf $F; done
find %i -name '*.egg-info' -exec rm {} \;

# Generate dependencies-setup.{sh,csh} so init.{sh,csh} picks full environment.
mkdir -p %i/etc/profile.d
: > %i/etc/profile.d/dependencies-setup.sh
: > %i/etc/profile.d/dependencies-setup.csh
for tool in $(echo %{requiredtools} | sed -e's|\s+| |;s|^\s+||'); do
  root=$(echo $tool | tr a-z- A-Z_)_ROOT; eval r=\$$root
  if [ X"$r" != X ] && [ -r "$r/etc/profile.d/init.sh" ]; then
    echo "test X\$$root != X || . $r/etc/profile.d/init.sh" >> %i/etc/profile.d/dependencies-setup.sh
    echo "test X\$$root != X || source $r/etc/profile.d/init.csh" >> %i/etc/profile.d/dependencies-setup.csh
  fi
done

%post
%{relocateConfig}etc/profile.d/dependencies-setup.*sh
