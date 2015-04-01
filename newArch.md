## Set up environment

	ARCH=<your-architecture>
	# ARCH=slc6_amd64_gcc491
	REPOSITORY=<your-repository>
	# REPOSITORY=cms
	BOOTSTRAP_VER=BOOTSTRAP_$ARCH
	HERE=/build/${USER}
	# HERE=/build1/${USER}

Get the correct PKGTOOLS and CMSDIST.

	rm -rf $HERE/build-$BOOTSTRAP_VER
	mkdir -p $HERE/build-$BOOTSTRAP_VER
	cd $HERE/build-$BOOTSTRAP_VER
	git clone git@github.com:cms-sw/cmsdist CMSDIST
	git clone git@github.com:cms-sw/pkgtools PKGTOOLS

## Building the initial RPM

Before you can develop a set of externals for a given architecture, you need to build a standalone version of RPM which has all the required patches to cope with CMS deployment environment.


	sh -e PKGTOOLS/build_rpm.sh -j 20 --arch $ARCH --prefix $HERE/build-$BOOTSTRAP_VER/rpmsw > build_rpm.log 2>&1

If any changes are required to build_rpm.sh commit them, tag and start back from scratch.

Building and testing the bootstrap kit

Then you can build and upload the bootstrap kit:

	export OLD_PATH=$PATH
	export OLD_LIBRARY_PATH=$LD_LIBRARY_PATH
	# export OLD_LIBRARY_PATH=$DYLD_FALLBACK_LIBRARY_PATH
	export PATH=$HERE/build-$BOOTSTRAP_VER/rpmsw/bin:$PATH
	export LD_LIBRARY_PATH=$HERE/build-$BOOTSTRAP_VER/rpmsw/lib:$LD_LIBRARY_PATH
	# export DYLD_FALLBACK_LIBRARY_PATH=$HERE/build-$BOOTSTRAP_VER/rpmsw/lib:$DYLD_FALLBACK_LIBRARY_PATH
	screen -L PKGTOOLS/cmsBuild --no-bootstrap --repository $REPOSITORY --arch $ARCH --work-dir b -j 20 upload bootstrap-driver cms-common lcg-dummy local-cern-siteconf

And then copy the bootstrap and the rest to the repository:

	scp b/SOURCES/external/apt/*/cmsos cmsbuild@cmsrep.cern.ch:/data/cmssw/$REPOSITORY.$USER/
	scp b/$ARCH/external/bootstrap-driver/`ls -rt b/$ARCH/external/bootstrap-driver/ | tail -1`/$ARCH-driver.txt cmsbuild@cmsrep.cern.ch:/data/cmssw/$REPOSITORY.$USER
	scp b/$ARCH/external/apt/`ls -rt b/$ARCH/external/apt/ | tail -1`/bin/bootstrap.sh cmsbuild@cmsrep.cern.ch:/data/cmssw/$REPOSITORY.$USER

Check the build is fine by doing:

	PATH=$OLD_PATH LD_LIBRARY_PATH=$OLD_LIBRARY_PATH screen -L PKGTOOLS/cmsBuild --repository $REPOSITORY.$USER --arch $ARCH --builders 2 --work-dir test -j 5 build cmssw-tool-conf
	# PATH=$OLD_PATH DYLD_FALLBACK_LIBRARY_PATH=$OLD_LIBRARY_PATH screen -L  PKGTOOLS/cmsBuild --repository $REPOSITORY.$USER --arch $ARCH --builders 2 --work-dir test -j 10 build cmssw-tool-conf

## Final upload

Upload the bootstrap kit to the repository:

	screen -L PKGTOOLS/cmsBuild --no-bootstrap --repository $REPOSITORY --arch $ARCH --work-dir b -j 20 --sync-back upload bootstrap-driver cms-common lcg-dummy local-cern-siteconf
	scp b/$ARCH/external/bootstrap-driver/`ls -rt b/$ARCH/external/bootstrap-driver/ | tail -1`/$ARCH-driver.txt cmsbuild@cmsrep.cern.ch:/data/cmssw/$REPOSITORY

* Notice you should never use a =PKGTOOLS= tag lesser than =V00-21-01= to do that.*

## Installing the bootstrap kit (Linux only)

Ask to Andreas Pfeiffer (at CERN) to create the volumes for the new architecture. Check they are available by doing:

	fs lq /afs/cern.ch/cms/$ARCH

which should give you an empty afs volume of 20GB.

After that, login to the server which has the local copy of the rpm database:

	ssh -l cmsbuild <machine-with-rpm-database>
	# ssh -l cmsbuild vocms155.cern.ch # SLC5
	# ssh -l cmsbuild vocms117.cern.ch # SLC6
	setenv ARCH <your-new-arch>
	# setenv ARCH slc5_amd64_gcc462
	# setenv ARCH slc6_amd64_gcc462
	setenv SYNCUSER <your-old-username>
	# setenv SYNCUSER eulisse
	setenv AFS_INSTALLATION_PATH /afs/.cern.ch/cms
	setenv LOCAL_DB /build/cmsbuild/$ARCH/`hostname`
	mkdir -p /build/cmsbuild/install-$ARCH/bootstraptmp
	cd /build/cmsbuild/install-$ARCH
	rm -rf $AFS_INSTALLATION_PATH/bootstraptmp
	ln -sf /build/cmsbuild/install-$ARCH/bootstraptmp $AFS_INSTALLATION_PATH/bootstraptmp 
	curl -o bootstrap.$ARCH.sh http://cmsrep.cern.ch/cmssw/cms/bootstrap.sh
	sh -ex bootstrap.$ARCH.sh -arch $ARCH -path $AFS_INSTALLATION_PATH setup
	mkdir -p $LOCAL_DB
	cp -r $AFS_INSTALLATION_PATH/$ARCH/var/lib/rpm $LOCAL_DB/rpm
	mv $AFS_INSTALLATION_PATH/$ARCH/var/lib/rpm $AFS_INSTALLATION_PATH/$ARCH/var/lib/rpm.original
	ln -s  $LOCAL_DB/rpm $AFS_INSTALLATION_PATH/$ARCH/var/lib/rpm
	/afs/cern.ch/cms/sdt/internal/scripts/requestRelVolumesSync.py --platform $ARCH --user $SYNCUSER  
