### RPM external llvm 3.0
## INITENV +PATH LD_LIBRARY_PATH %i/lib64

# s/#/S/ to use the official version.
Source0: http://llvm.org/releases/%realversion/llvm-%realversion.tar.gz
Source1: http://llvm.org/releases/%realversion/clang-%realversion.tar.gz 
# SVN builds. Comment out to use the official version.
#Source0: svn://llvm.org/svn/llvm-project/llvm/tags/RELEASE_29/rc3/?scheme=http&module=llvm-%realversion&output=/llvm-%realversion.tgz
#Source1: svn://llvm.org/svn/llvm-project/cfe/tags/RELEASE_29/rc3/?scheme=http&module=clang-%realversion&output=/clang-%realversion.tgz
Patch0: llvm-3.0-custom-gcc

%prep
%setup -T -b0 -n llvm-%realversion.src
%setup -T -D -a1 -c -n llvm-%realversion.src/tools
mv clang-%realversion.src clang
cd clang
case %cmsos in
  slc*)
%patch0 -p1
  ;;
esac
%setup -T -D -n llvm-%realversion.src

%build
mkdir objs ; cd objs
../configure --prefix=%i --enable-optimized
make %makeprocesses

%install
cd objs
make install
# Fix up a perl path
perl -p -i -e 's|^#!.*perl(.*)|#!/usr/bin/env perl$1|' %i/bin/llvm-config
