### RPM cms cms-cvs-utils 1.0
## INITENV ALIAS_SH project source %i/bin/projch.sh
## INITENV ALIAS_SH cmscvsroot source %i/bin/cmscvsroot.sh
## INITENV ALIAS_CSH project source %i/bin/projch.csh
## INITENV ALIAS_CSH cmscvsroot source %i/bin/cmscvsroot.csh
## INITENV ALIAS clcommit %i/bin/clcommit.sh
Source: none

%prep
%build
%install
mkdir -p %instroot/%cmsplatf/etc/profile.d/
mkdir -p %i/bin

cat << \EOF_PROJCH_SH > %i/bin/projch.sh
# Check if theres any argument
#
if [ $# -gt 2 ]; then
  echo "Usage : project project_name [version]";
else

version="current"
VERSIO="current"
if [ $# = 2 ]; then
  version=$2
  VERSIO=$2
fi

export VERSIO
#CVS STUFF 
cvsbase=":gserver:cmscvs.cern.ch:/cvs_server/repositories"
projectname=$1
case $projectname in
    CMSSW )
    cvsbase=":gserver:cmscvs.cern.ch:/cvs_server/repositories"
    ;;
    * )
    cvsbase=":gserver:isscvs.cern.ch/local/reps"
    projectname=`echo $projectname | tr "[A-Z]" "[a-z]"`
    ;;
esac
    
CVSROOT="${cvsbase}/$projectname"; export CVSROOT

#SRT STUFF
#if [ -f $CMS_PATH/OO/Software/$1/releases/$version/SoftRelTools/SRTstartup.sh ]; then
# BFCURRENT=$version
# export BFCURRENT
# . $CMS_PATH/OO/Software/$1/releases/$version/SoftRelTools/SRTstartup.sh
#fi
fi
EOF_PROJCH_SH

cat << \EOF_PROJCH_CSH > %{i}/bin/projch.csh
# Check if theres any argument
#
# if ( ($# > 1) | ($# < 1) ) then
if ( ($# > 2) | ($# < 1) ) then
  echo "Usage : project project_name [version]"
else

set version="current"
setenv VERSIO current
if ( $# == 2 ) then
  set version=$argv[2]
  setenv VERSIO $argv[2]
endif

#CVS Stuff
set projectname = $argv[1]
set cvsbase = ":gserver:cmscvs.cern.ch:/cvs_server/repositories"
if ( $argv[1] != "CMSSW" ) then
    set cvsbase=":gserver:isscvs.cern.ch/local/reps"
    set projectname=`echo $projectname | tr "[A-Z]" "[a-z]"`
endif

setenv CVSROOT "${cvsbase}/$projectname"

#SRT STUFF
#if ( -f $CMS_PATH/OO/Software/$argv[1]/releases/${version}/SoftRelTools/SRTstartup.csh ) then
# setenv BFCURRENT $version
# source $CMS_PATH/OO/Software/$argv[1]/releases/${version}/SoftRelTools/SRTstartup.csh
#endif
endif
EOF_PROJCH_CSH

cat << \EOF_CMSCVSROOT_SH > %i/bin/cmscvsroot.sh
# Check if theres any argument
#
if [ $# -gt 2 ]; then
  echo "Usage : cmscvsroot project_name";
else

#CVS STUFF 
cvsbase=":pserver:anonymous@cmscvs.cern.ch:/cvs_server/repositories"
projectname=$1
case $1 in
    CMSSW )
        cvsbase=":pserver:anonymous@cmscvs.cern.ch:/cvs_server/repositories"
    ;;
    * )
        cvsbase=":pserver:anonymous@isscvs.cern.ch/local/reps"
        projectname=`echo $projectname | tr "[A-Z]" "[a-z]"`
    ;;
esac

CVSROOT="${cvsbase}/$1"; export CVSROOT

fi
EOF_CMSCVSROOT_SH

cat << \EOF_CMSCVSROOT_CSH > %i/bin/cmscvsroot.csh
# Check if theres any argument
#
if ( ($# > 1) | ($# < 1) ) then
  echo "Usage : cmscvsroot project_name"
else

#CVS Stuff
set projectname = $argv[1]
set cvsbase = ":pserver:anonymous@cmscvs.cern.ch:/cvs_server/repositories"
if ( $argv[1] != "CMSSW" ) then
    set cvsbase=":pserver:anonymous@isscvs.cern.ch/local/reps"
    set projectname=`echo $projectname | tr "[A-Z]" "[a-z]"`
endif
setenv CVSROOT "${cvsbase}/$argv[1]"

endif
EOF_CMSCVSROOT_CSH

cat << \EOF_CLCOMMIT > %i/bin/clcommit.sh
#! /bin/sh

# commit version 0.9.4

# Copyright (C) 1999, 2000, Free Software Foundation

# This script is Free Software, and it can be copied, distributed and
# modified as defined in the GNU General Public License.  A copy of
# its license can be downloaded from http://www.gnu.org/copyleft/gpl.html

# Originally by Gary V. Vaughan <gvaughan@oranda.demon.co.uk>
# Heavily modified by Alexandre Oliva <oliva@dcc.unicamp.br>

# This scripts eases checking in changes to CVS-maintained projects
# with ChangeLog files.  It will check that there have been no
# conflicting commits in the CVS repository and print which files it
# is going to commit to stderr.  A list of files to compare and to
# check in can be given in the command line.  If it is not given, all
# files in the current directory (and below, unless `-l' is given) are
# considered for check in.

# The commit message will be extracted from the differences between a
# file named ChangeLog* in the commit list, or named after -C, and the
# one in the repository (unless a message was specified with `-m' or
# `-F').  An empty message is not accepted (but a blank line is).  If
# the message is acceptable, it will be presented for verification
# (and possible edition) using the $PAGER environment variable (or
# `more', if it is not set, or `cat', if the `-f' switch is given).
# If $PAGER exits successfully, the modified files (at that moment)
# are checked in, unless `-n' was specified, in which case nothing is
# checked in.

# usage: commit [-v] [-h] [-f] [-l] [-n] [-q] [-z N] [-C ChangeLog_file]
#               [-m msg|-F msg_file] [--] [file|dir ...]

# -f      --fast        don't check (unless *followed* by -n), and just 
#         --force       display commit message instead of running $PAGER
# -l      --local       don't descend into subdirectories
# -m msg  --message=msg set commit message
#         --msg=msg     same as -m
# -F file --file=file   read commit message from file
# -C file --changelog=file extract commit message from specified ChangeLog
# -n      --dry-run     don't commit anything
# -q      --quiet       run cvs in quiet mode
# -zN     --compress=N  set compression level (0-9, 0=none, 9=max)
# -v      --version     print version information
# -h,-?   --help        print short or long help message

name=commit
: ${CVS=cvs}
cvsopt=
updateopt=
commitopt=
dry_run=false
commit=:
update=:
log_file="${TMPDIR-/tmp}/commitlog.$$"

rm -f "$log_file"
trap 'rm -f "$log_file"; exit 1' 1 2 15

# this just eases exit handling
main_repeat=":"
while $main_repeat; do

repeat="test $# -gt 0"
while $repeat; do
    case "$1" in
    -f|--force|--fast)
        update=false
        PAGER=cat
        shift
        ;;
    -l|--local)
        updateopt="$updateopt -l"
        commitopt="$commitopt -l"
        shift
        ;;
    -m|--message|--msg)
        if test $# = 1; then
            echo "$name: missing argument for $1" >&2
            break
        fi
        if test -f "$log_file"; then
            echo "$name: you can have at most one of -m and -F" >&2
            break
        fi
        shift
        echo "$1" > "$log_file"
        shift
        ;;
    -F|--file)
        if test -f "$log_file"; then
            echo "$name: you can have at most one of -m and -F" >&2
            break
        fi
        if test $# = 1; then
            echo "$name: missing argument for $1" >&2
            break
        fi
        shift
        if cat < "$1" > "$log_file"; then :; else
            break
        fi
        shift
        ;;
    -C|--[cC]hange[lL]og)
        if test $# = 1; then
            echo "$name: missing argument for $1" >&2
            break
        fi
        shift
        if test ! -f "$1"; then
            echo "$name: ChangeLog file \`$1' does not exist" >&2
            break
        fi
        ChangeLog="$1"
        ;;
    -n|--dry-run)
        PAGER=cat
        commit=false
        update=true
        shift
        ;;
    -q|--quiet)
        cvsopt="$cvsopt -q"
        shift
        ;;
    -z|--compress)
        if test $# = 1; then
            echo "$name: missing argument for $1" >&2
            break
        fi
        case "$2" in
        [0-9]) :;;
        *)  echo "$name: invalid argument for $1" >&2
            break
            ;;
        esac
        cvsopt="$cvsopt -z$2"
        shift
        shift
        ;;

    -m*|-F*|-C*|-z*)
        opt=`echo "$1" | sed '1s/^\(..\).*$/\1/;q'`
        arg=`echo "$1" | sed '1s/^-[a-zA-Z0-9]//'`
        shift
        set -- "$opt" "$arg" ${1+"$@"}
        ;;
    --message=*|--msg=*|--file=*|--[Cc]hange[Ll]og=*|--compress=*)
        opt=`echo "$1" | sed '1s/^\(--[^=]*\)=.*/\1/;q'`
        arg=`echo "$1" | sed '1s/^--[^=]*=//'`
        shift
        set -- "$opt" "$arg" ${1+"$@"}
        ;;

    -v|--version)
        sed '/^# '$name' version /,/^# Heavily modified by/ { s/^# //; p; }; d' < $0
        exit 0
        ;;
    -\?|-h)
        sed '/^# usage:/,/# -h/ { s/^# //; p; }; d' < $0 &&
        echo
        echo "run \`$name --help | more' for full usage"
        exit 0
        ;;
    --help)
        sed '/^# '$name' version /,/^[^#]/ { /^[^#]/ d; s/^# //; p; }; d' < $0
        exit 0
        ;;
    --)
        shift
        repeat=false
        ;;
    -*)
        echo "$name: invalid flag $1" >&2
        break
        ;;
    *)
        repeat=false
        ;;
    esac
done
# might have used break 2 within the previous loop, but so what
$repeat && break

$update && \
if echo "$name: checking for conflicts..." >&2
   ($CVS $cvsopt -q -n update $updateopt ${1+"$@"} 2>/dev/null \
    | while read line; do
        echo "$line"
        echo "$line" >&3
      done | grep '^C') 3>&1 >/dev/null; then
  echo "$name: some conflicts were found, aborting..." >&2
  break
fi

if test ! -f "$log_file"; then
  if test -z "$ChangeLog"; then
    for f in ${1+"$@"}; do
      case "$f" in
      ChangeLog* | */ChangeLog*)
        if test -z "$ChangeLog"; then
            ChangeLog="$f"
        else
            echo "$name: multiple ChangeLog files: $ChangeLog and $f" >&2
            break
        fi
        ;;
      esac
    done
  fi

  echo "$name: checking commit message..." >&2
  $CVS $cvsopt diff -u ${ChangeLog-ChangeLog} \
  | while read line; do
      case "$line" in
      "--- "*) :;;
      "-"*)
        echo "$name: *** Warning: the following line in ChangeLog diff is suspicious:" >&2
        echo "$line" | sed 's/^.//' >&2;;
      "+ "*)
        echo "$name: *** Warning: lines should start with tabs, not spaces; ignoring line:" >&2
        echo "$line" | sed 's/^.//' >&2;;
      "+") echo;;
      "+        "*) echo "$line";;
      esac
    done \
  | sed -e 's,\+        ,,' -e '/./p' -e '/./d' -e '1d' -e '$d' > "$log_file" \
  || break
# The sed script above removes "+TAB" from the beginning of a line, then
# deletes the first and/or the last line, when they happen to be empty
fi

if grep '[^     ]' < "$log_file" > /dev/null; then :; else
  echo "$name: empty commit message, aborting" >&2
  break
fi

if grep '^$' < "$log_file" > /dev/null; then
  echo "$name: *** Warning: blank lines should not appear within a commit messages." >&2
  echo "$name: *** They should be used to separate distinct commits." >&2
fi

${PAGER-more} "$log_file" || break

sleep 1 # give the user some time for a ^C

# Do not check for empty $log_file again, even though the user might have
# zeroed it out.  If s/he did, it was probably intentional.

if $commit; then
    echo " $CVS $cvsopt commit $commitopt -F $log_file ${1+"$@"} || break"
  $CVS $cvsopt commit $commitopt -F $log_file ${1+"$@"} || break
fi

main_repeat=false
done

rm -f "$log_file"

# if main_repeat was not set to `false', we failed
$main_repeat && exit 1
exit 0
EOF_CLCOMMIT

chmod +x %i/bin/projch.sh
chmod +x %i/bin/projch.csh
chmod +x %i/bin/cmscvsroot.sh
chmod +x %i/bin/cmscvsroot.csh
chmod +x %i/bin/clcommit.sh

ln -sf %i/etc/profile.d/init.sh %instroot/%cmsplatf/etc/profile.d/S00cms-cvs-utils.sh 
ln -sf %i/etc/profile.d/init.csh %instroot/%cmsplatf/etc/profile.d/S00cms-cvs-utils.csh

%files
%i
%instroot/%cmsplatf/etc/profile.d/S00cms-cvs-utils.sh
%instroot/%cmsplatf/etc/profile.d/S00cms-cvs-utils.csh

%post
perl -p -i -e 's|(.*setenv.*)|#$1|' $RPM_INSTALL_PREFIX/%pkgrel/etc/profile.d/init.csh
perl -p -i -e 's|(.*export.*)|#$1|' $RPM_INSTALL_PREFIX/%pkgrel/etc/profile.d/init.sh
ln -sf $RPM_INSTALL_PREFIX/%pkgrel/etc/profile.d/init.sh $RPM_INSTALL_PREFIX/%cmsplatf/etc/profile.d/S00cms-cvs-utils.sh 
ln -sf $RPM_INSTALL_PREFIX/%pkgrel/etc/profile.d/init.csh $RPM_INSTALL_PREFIX/%cmsplatf/etc/profile.d/S00cms-cvs-utils.csh
