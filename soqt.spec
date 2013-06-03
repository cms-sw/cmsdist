### RPM external soqt 1.4.1
Requires: qt
Requires: coin
Source: ftp://ftp.coin3d.org/pub/coin/src/all/SoQt-%{realversion}.tar.gz
# FIXME: forget about the patch for the time being. 
# I need to ask lassi where to find it. 
Patch0: soqt
Patch1: soqt-ptr-fix

%prep
%setup -n SoQt-%{realversion}
%patch0
%patch1 -p2

%build
case %cmsplatf in
  osx*) threads= cfgflags="-without-framework --without-x" ;;
  *)      threads=-pthread cfgflags= ;;
esac

export QTDIR=$QT_ROOT
export CONFIG_QTLIBS="-L$QT_ROOT/lib -L$COIN_ROOT/lib -lQt3Support -lQtCore -lQtGui -lQtOpenGL -lQtDesigner $libs"
export DYLD_LIBRARY_PATH=$QTDIR/lib:$DYLD_LIBRARY_PATH
export LD_LIBRARY_PATH=$QTDIR/lib:$LD_LIBRARY_PATH

which c++
./configure --prefix=%i --with-coin=$COIN_ROOT \
            --with-qt=$QT_ROOT --disable-dependency-tracking \
            --disable-libtool-lock $cfgflags \
            CXX="c++ $threads"

make %makeprocesses

%install
make install
