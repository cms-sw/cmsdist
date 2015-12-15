### RPM external oracle 11.2.0.3.0__10.2.0.4.0
## INITENV SET ORACLE_HOME %i
## INITENV +PATH SQLPATH %i/bin

# Notice that we have a dummy package version because the mac and linux clients
# are not in sync. Moreover, because it's a binary only package we need to
# point to different blobs for different architecture.
# Do not even think about commenting out one of the sources, simply because
# it's not needed for your platform.
# These are the original ZIP files from oracle. Do not use anything else.
%define copydate        20120309
%define mirrordir       http://cmsrep.cern.ch/cmssw/oracle-mirror

%define macdir          instantclient_10_2
%define macarch         macosx-x64
%define macversion      10.2.0.4.0

%define linuxdir        instantclient_11_2
%define linuxarch       linux.x64
%define linuxversion    11.2.0.3.0

# The ZIP files contain overlapping files, and by default 'unzip' wants to
# ask about whether to overwrite files or not. This is really awkward if you
# run the build in a terminal, so force overwrites always.
%define __unzip         unzip -o

Source0: %mirrordir/%copydate-instantclient-basic-%macversion-%macarch.zip
Source1: %mirrordir/%copydate-instantclient-basiclite-%macversion-%macarch.zip
Source2: %mirrordir/%copydate-instantclient-jdbc-%macversion-%macarch.zip
Source3: %mirrordir/%copydate-instantclient-sdk-%macversion-%macarch.zip
Source4: %mirrordir/%copydate-instantclient-sqlplus-%macversion-%macarch.zip

Source5: %mirrordir/%copydate-instantclient-basic-%linuxarch-%linuxversion.zip
Source6: %mirrordir/%copydate-instantclient-basiclite-%linuxarch-%linuxversion.zip
Source7: %mirrordir/%copydate-instantclient-jdbc-%linuxarch-%linuxversion.zip
Source8: %mirrordir/%copydate-instantclient-sdk-%linuxarch-%linuxversion.zip
Source9: %mirrordir/%copydate-instantclient-sqlplus-%linuxarch-%linuxversion.zip

Source10: oracle-license
Requires: fakesystem 

%define islinux %(case $(uname -s) in (Linux) echo 1 ;; (*) echo 0 ;; esac)
%define isamd64 %(case %{cmsplatf} in (*_amd64_*) echo 1 ;; (*) echo 0 ;; esac)

%prep
# We unpack only the sources for the architecture we are working on.  Do not
# change this to unpack all the architectures.  Notice also that you cannot put
# ;; on the same line as the %%setup macro, because the latter will swallow it
# as part of the arguments.
# Notice that we are forced to use rpm macros because %%setup registers the 
# final directory to use as the one of the last %%setup happening.
rm -fr instantclient_*
%if %(case %cmsos in (osx*) echo true ;; (*) echo false ;; esac) == true
%setup -D -T -b 0 -n %macdir %copydate-instantclient-basic-%macversion-%macarch.zip
%setup -D -T -b 1 -n %macdir %copydate-instantclient-basiclite-%macversion-%macarch.zip
%setup -D -T -b 2 -n %macdir %copydate-instantclient-jdbc-%macversion-%macarch.zip
%setup -D -T -b 3 -n %macdir %copydate-instantclient-sdk-%macversion-%macarch.zip
%setup -D -T -b 4 -n %macdir %copydate-instantclient-sqlplus-%macversion-%macarch.zip
%endif

%if %islinux
%if %isamd64
%setup -D -T -b 5 -n %linuxdir %copydate-instantclient-basic-%linuxarch-%linuxversion.zip
%setup -D -T -b 6 -n %linuxdir %copydate-instantclient-basiclite-%linuxarch-%linuxversion.zip
%setup -D -T -b 7 -n %linuxdir %copydate-instantclient-jdbc-%linuxarch-%linuxversion.zip
%setup -D -T -b 8 -n %linuxdir %copydate-instantclient-sdk-%linuxarch-%linuxversion.zip
%setup -D -T -b 9 -n %linuxdir %copydate-instantclient-sqlplus-%linuxarch-%linuxversion.zip
%endif # isamd64
%endif # islinux

%build
chmod a-x sdk/include/*.h *.sql

%install
mkdir -p %i/{bin,lib,java,demo,include,doc}
cp %_sourcedir/oracle-license    %i/oracle-license
mv *_README sdk/*_README         %i/doc
mv lib*                          %i/lib
mv glogin.sql                    %i/bin
mv *.jar sdk/*.zip               %i/java
mv sdk/demo/*                    %i/demo
mv sdk/include/*                 %i/include

for f in sqlplus adrci genezi uidrvci sdk/ott; do
  [ -f $f ] || continue
  mv $f %i/bin
done

cd %i/lib
for f in lib*.{dylib,so}.[0-9]*; do
  [ -f $f ] || continue
  dest=$(echo $f | sed 's/\.[.0-9]*$//')
  rm -f $dest
  ln -s $f $dest
done
