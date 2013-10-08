---
title: CMSDIST
layout: default
related:
 - { name: Home, link: "index.html" }
 - { name: Project, link: "https://github.com/cms-sw/cmsdist" }
 - { name: Feedback, link: "https://github.com/cms-sw/cmsdist/issues/new" }
---

This is the documentation page for CMSDIST, CMS SW distribution recipes.

* auto-gen TOC:
{:toc}

## Branch structure

Each release series should have a branch called:

    IB/<CMSSW_x_y_X>/stable

where `<CMSSW_x_y_Z>` is some release queue, e.g.:

    IB/CMSSW_6_2_X/stable 

We will call this branch the "stable CMSDIST branch for the release queue".
This branch is the one used for the production architecture of such a release.
For example the `CMSSW_6_2_X` release on `slc5_amd64_gcc472` would use such a
branch.

Such a branch will contain a file called `config.map` which consist of the
mapping between architectures and the `PKGTOOLS` and `CMSDIST` tags for that
release on the given architecture. The file consists of one or more lines with
the following format.

    SCRAM_ARCH=<architecture>;PKGTOOLS_TAG=<pkgtools-ref>;CMSDIST_TAG=<cmsdist-ref>

where:

* `<architecture>` is the SCRAM architecture being considered, e.g.
  `slc5_amd64_gcc472`.
* `<pkgtools-ref>` is a reference to the PKGTOOLS branch to be used for
  building the release associated with the given branch on the specified
  architecture.
* `<pkgtools-ref>` is a reference to the CMSDIST branch to be used for building
  the release associated with the given branch on the specified architecture.

an example of such a file is:

    SCRAM_ARCH=slc5_amd64_gcc472;PKGTOOLS_TAG=V00-21-XX;CMSDIST_TAG=IB/CMSSW_6_2_X/stable
    SCRAM_ARCH=slc6_amd64_gcc472;PKGTOOLS_TAG=V00-22-XX;CMSDIST_TAG=IB/CMSSW_6_2_X/devel-gcc472
    SCRAM_ARCH=slc6_amd64_gcc480;PKGTOOLS_TAG=V00-22-XX;CMSDIST_TAG=IB/CMSSW_6_2_X/slc6_amd64_gcc480
    SCRAM_ARCH=fc18_armv7hl_gcc480;PKGTOOLS_TAG=V00-21-XX;CMSDIST_TAG=IB/CMSSW_6_2_X/fc18_armv7hl_gcc480
    SCRAM_ARCH=osx108_amd64_gcc472;PKGTOOLS_TAG=V00-21-XX;CMSDIST_TAG=IB/CMSSW_6_2_X/devel-gcc472
    SCRAM_ARCH=osx107_amd64_gcc472;PKGTOOLS_TAG=V00-21-XX;CMSDIST_TAG=IB/CMSSW_6_2_X/devel-gcc472

in this particular case you see that `slc6_amd64_gcc472`,
`osx108_amd64_gcc472`, `osx107_amd64_gcc472` share the same ref for the CMSDIST
tag.

**While adding special branches for development architectures is allowed, this
  should not be abused and the goal should be to minimize the number of
  branches required.**

## Proposing a new addition

### One time setup

If you have not done it yet, register to github ([click here on how to do
it][register-faq]).

Fork the CMSDIST repository by [clicking
here](https://github.com/cms-sw/cmsdist/fork). Note down the url of your
repository, you'll need it to propose your changes.

### For every new feature / bug fix you want to propose.

0) Setup initial parameters:

    CMSSW=<RELEASE>
    # CMSSW=CMSSW_5_2_X
    # CMSSW=CMSSW_5_3_X
    # CMSSW=CMSSW_6_1_X
    # CMSSW=CMSSW_6_2_X
    # CMSSW=CMSSW_7_0_X
    ARCH=<ARCH>
    # ARCH=slc5_amd64_gcc462
    # ARCH=slc5_amd64_gcc472
    # ARCH=slc5_amd64_gcc481
    # ARCH=slc6_amd64_gcc472
    # ARCH=slc6_amd64_gcc481
    # ARCH=osx106_amd64_gcc462
    # ARCH=osx107_amd64_gcc462
    # ARCH=osx107_amd64_gcc472
    # ARCH=osx108_amd64_gcc472
    # ARCH=osx108_amd64_gcc481

    # Set the partition used for building.
    # Partition depends on the machine (/build1 and /build might be available on Linux,
    # and /build1 (/Volumes/build1) on Mac OS X)
    case $ARCH in
      slc*) BUILDDIR=/build ;;
      osx*) BUILDDIR=/build1 ;;
    esac

1) Create build area and prepare CMSDIST and PKGTOOLS:

      HERE=${BUILDDIR}/${USER}
      DATETIME=$(date +'%Y%m%d_%H%M')
      TOPDIR=${HERE}/ext/${CMSSW}/${DATETIME}
      mkdir -p $TOPDIR
      cd $TOPDIR
      git clone git@github.com:cms-sw/cmsdist.git CMSDIST
      pushd CMSDIST
        eval $(git show IB/$CMSSW/stable:config.map | grep $ARCH)
        git checkout $CMSDIST_TAG
      popd
      git clone -b $PKGTOOLS_TAG git@github.com:cms-sw/pkgtools.git PKGTOOLS

2) Edit CMSDIST, build and test the external:

      pushd CMSDIST
        <edit spec file>
        git commit <spec file>
      popd
      screen -L time PKGTOOLS/cmsBuild -i a -a $ARCH --builders 4 -j $(($(getconf _NPROCESSORS_ONLN) * 2)) build cmssw-tool-conf

3) Once you are satisfied with the above push your changes to your repository:

      git remote add $USER <your-cmsdist-fork>
      git push $USER $CMSDIST_TAG

4) [Create a Pull Request from your repository to the official one][github-pull].

All the pending pull requests to branches of the form `IB/CMSSW_X_Y_Z/stable`
will be reviewed in the following ORP meeting and possibly approved.

## Build externals for a given release:

Let's assume you want to build externals for the a given release series:

    CMSSW=<release-queue>
    # CMSSW=CMSSW_5_2_X
    # CMSSW=CMSSW_5_3_X
    # CMSSW=CMSSW_6_1_X
    # CMSSW=CMSSW_6_2_X

You can find the list of all the required architecture by doing:

    curl https://raw.github.com/cms-sw/cmsdist/IB/$CMSSW/stable/config.map
    
For every architecture mentioned there you'll have to repeat the following:

0) Prepare the environment:

    export CVSROOT=:gserver:cmssw.cvs.cern.ch:/local/reps/CMSSW
    CMSSW=<RELEASE>
    # CMSSW=CMSSW_5_2_X
    # CMSSW=CMSSW_5_3_X
    # CMSSW=CMSSW_6_1_X
    # CMSSW=CMSSW_6_2_X
    ARCH=<ARCH>
    # ARCH=slc5_amd64_gcc462
    # ARCH=slc5_amd64_gcc472
    # ARCH=slc6_amd64_gcc472
    # ARCH=slc6_amd64_gcc480
    # ARCH=osx106_amd64_gcc462
    # ARCH=osx107_amd64_gcc462
    # ARCH=osx107_amd64_gcc472
    # ARCH=osx108_amd64_gcc472

    # Set the partition used for building.
    # Partition depends on the machine (/build1 and /build might be available on Linux,
    # and /build1 (/Volumes/build1) on Mac OS X)
    case $ARCH in
      slc*) BUILDDIR=/build ;;
      osx*) BUILDDIR=/build1 ;;
    esac

1) Create build area and prepare CMSDIST and PKGTOOLS:

      HERE=${BUILDDIR}/${USER}
      DATETIME=$(date +'%Y%m%d_%H%M')
      URL="https://raw.github.com/cms-sw/cmsdist/IB/$CMSSW/stable/config.map"
      eval $(curl -s -k "${URL}" | grep $ARCH)
      TOPDIR=${HERE}/ext/${CMSSW}/${DATETIME}
      mkdir -p $TOPDIR
      cd $TOPDIR
      git clone -b $CMSDIST_TAG git@github.com:cms-sw/cmsdist.git CMSDIST
      git clone -b $PKGTOOLS_TAG git@github.com:cms-sw/pkgtools.git PKGTOOLS

2) Build the externals:

      screen -L time PKGTOOLS/cmsBuild -i a -a $ARCH --builders 4 -j $(($(getconf _NPROCESSORS_ONLN) * 2)) build cmssw-tool-conf

3) Validate the externals by going through the [troubleshooting
checklist](troubleshooting-checklist.html).

4) Upload the externals to the repository. Please make sure you use a tag later
   than V00-21-01 for doing the uploads. Uploads are done for each architecture
   (incl Mac OS X).
   
      eval `ssh-agent`
      ssh-add
      screen -L time PKGTOOLS/cmsBuild -i a -a $ARCH --sync-back upload cmssw-tool-conf

## Installing externals @ CERN.

Follow up the instructions
[here](https://twiki.cern.ch/twiki/bin/view/CMS/SDTHowToBuildExternalTools#Installing_Re_syncing_AFS_Volume)
(protected to avoid leaking CERN infrastructure details, do not create pull
requests for it).

## Contributing to these pages.

These pages are created using github pages. To contribute:

* Fork the cmsdist repository
* Checkout the `gh-pages` branch
* Amend
* Push changes to your local repository
* Open a pull request

[register-faq]: http://cms-sw.github.io/cmssw/faq.html#how_do_i_subscribe_to_github
[github-pull]:      https://github.com/cms-sw/cmsdist/pull/new/master
