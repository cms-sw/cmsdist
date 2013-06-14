### RPM external atlas 3.6.0
# NB: http://www.netlib.org/atlas/atlas-comm/msg00280.html
#     http://cvs.pld-linux.org/cgi-bin/cvsweb/SPECS/atlas.spec
Source: http://switch.dl.sourceforge.net/sourceforge/math-atlas/%n%v.tar.bz2
Requires: lapack

%prep
%setup -n ATLAS

%build
mergelibs() {
 destlib=$1; shift;
 for srclib; do ar x $srclib; done
 rm -f $destlib
 ar cr $destlib *.o
}

makesolib() {
 destlib=$1 srclib=$2 v=$3 so=$4
 basedestlib=$(basename $destlib)
 rm -f $destlib*
 gcc -shared `case $lib in *libpt*) echo -pthread ;; esac` \
   -o $destlib.$v -Wl,-soname,$basedestlib.$so \
   -Wl,--whole-archive $srclib -Wl,--no-whole-archive \
  `case $destlib in *f77* | *lapack* ) echo -lg2c;; esac` -lm
 (cd $(dirname $destlib) && ln -s $basedestlib.$v $basedestlib.$so)
 (cd $(dirname $destlib) && ln -s $basedestlib.$v $basedestlib)
}

case %cmsplatf in
  *ia32*  ) machtype=8;; # Pentium 4
  *amd64* ) machtype=4;; # 64 bit AMD Hammer
  *       ) machtype=1;; # Unknown
esac

cat > config.expect <<EOF
 log_file "config.expect.log"
 set finished 0
 set arch cms
 spawn ./xconfig -g $GCC_ROOT/bin/gcc -f $GCC_ROOT/bin/g77
 while {\$finished == 0} {
  set timeout 120
  expect {
   -nocase {Enter bit number \[2\]:}             {send "2\n"}
   -nocase {Enter number at top left of screen}  {send "99\n"}
   -nocase {Have you scoped the errata file\?}   {send "y\n"}
   -nocase {Are you ready to continue\?}         {send "y\n"}
   -nocase -re {Enter machine number \[.*\]: }   {send "$machtype\n"}
   -nocase {Are you using a cross-compiler\?}    {send "n\n"}
   -nocase {enable Posix threads support\?}      {send "y\n"}
   -nocase {use express setup\?}                 {send "y\n"}
   -nocase -re {Enter Architecture name \(ARCH\) \[.*\]} { send "%{cmsplatf}\n" }
   -nocase {Enter Maximum cache size}            { send "\n" }
   -nocase {Enter File creation delay in seconds} {send "0\n"}
   -nocase {Enter Top level ATLAS directory}     {send "\n"}
   -nocase {Enter Directory to build libraries in} {send "\n"}
   -nocase {Enter f77 compiler}                  {send "\n"}
   -nocase {Enter F77 Flags}                     {send "\n"}
   -nocase {Enter F77 linker}                    {send "\n"}
   -nocase {Enter F77 Link Flags}                {send "\n"}
   -nocase {Enter ANSI C compiler}               {send "\n"}
   -nocase {Enter C Flags \(CCFLAGS\)}           {send "\n"}
   -nocase {Enter C compiler for generated code} {send "\n"}
   -nocase {Enter C FLAGS \(MMFLAGS\)}           {send "\n"}
   -nocase {Enter C Linker}                      {send "\n"}
   -nocase {Enter C Link Flags}                  {send "\n"}
   -nocase {Enter Archiver \[}                   {send "\n"}
   -nocase {Enter Archiver flags}                {send "\n"}
   -nocase {Enter Ranlib}                        {send "\n"}
   -nocase {Enter BLAS library}                  {send "\n"}
   -nocase {Enter General and system libs}       {send "\n"}
   -nocase {kill old subdirectories\?}           {send "y\n"}
   -nocase {Tune the Level 1 BLAS\?}             {send "\n"}
   -nocase {use supplied default values for install\?} {send "y\n"}
   -nocase {Configuration completed successfully} {set finished 1}
   timeout                                       {puts timeout; exit 1}
  }
 }
 close
 exit
EOF
make xconfig
expect -f config.expect
rm -f config.expect

cd CONFIG
ln -s ATLrun.%cmsplatf ATLrun.%{cmsplatf}_so
cd ..

perl -p -i -e '
  s, (F77|CC|MM|XCC)FLAGS = (.*), ${1}FLAGS = $2 -fPIC,;
  s, ARCH = (.*), ARCH = ${1}_so,' \
  < Make.%{cmsplatf} > Make.%{cmsplatf}_so

for arch in %{cmsplatf} %{cmsplatf}_so; do
 case $arch in *_so ) laext=_pic ;; *) laext= bpfx= ;; esac

 make killall arch=$arch
 make startup arch=$arch
 make install arch=$arch

 for pfx in "" "pt"; do
   mkdir tmp; cd tmp
     mergelibs ../lib/$arch/lib${pfx}f77blas.a \
       ../lib/$arch/libatlas.a \
       ../lib/$arch/lib${pfx}f77blas.a
   cd ..; rm -fr tmp
 done
 mkdir tmp; cd tmp
   mergelibs ../lib/$arch/liblapack_atlas.a \
     $LAPACK_ROOT/lib/liblapack${laext}.a \
     ../lib/$arch/liblapack.a \
     ../lib/$arch/libcblas.a
 cd ..; rm -fr tmp
done

for lib in {,pt}cblas {,pt}f77blas lapack_atlas; do
 mkdir tmp; cd tmp
   makesolib \
     ../lib/%{cmsplatf}_so/lib$lib.so \
     ../lib/%{cmsplatf}_so/lib$lib.a \
     $(echo %v | awk -F. '{print $1 "." $2}') \
     $(echo %v | awk -F. '{print $1}')
 cd ..; rm -fr tmp
done

%install
mkdir -p %i/lib
(cd lib/%{cmsplatf}; tar -cf - lib{,pt}{c,f77}blas.a liblapack_atlas.a) | (cd %i/lib; tar -xvf -)
(cd lib/%{cmsplatf}_so; tar -cf - lib{,pt}{c,f77}blas.so* liblapack_atlas.so*) | (cd %i/lib; tar -xvf -)
tar -cf - include | (cd %i; tar -xvf -)
