### RPM external nspr-bootstrap 4.9.5
Source: https://ftp.mozilla.org/pub/mozilla.org/nspr/releases/v%{realversion}/src/nspr-%{realversion}.tar.gz
%define strip_files %{i}/lib

%define isamd64 %(case %{cmsplatf} in (*amd64*|*_mic_*) echo 1 ;; (*) echo 0 ;; esac)
%prep  
%setup -n nspr-%{realversion}

%build
pushd mozilla/nsprpub
CONF_OPTS="--disable-static --prefix=%{i} --build=%{_build} --host=%{_host}"
%if %isamd64
CONF_OPTS="${CONF_OPTS} --enable-64bit"
%endif

./configure ${CONF_OPTS}
make %{makeprocesses}
popd

%install
pushd mozilla/nsprpub
make install
popd

for x in `find %{i}/lib -type f -perm -u+x | grep -v -e "[.]pyc"`; 
do 
    if [ "X`file --mime $x | sed -e 's| ||g' | cut -d: -f2 | cut -d\; -f1`" = Xapplication/octet-stream ]
    then
      chmod +w $x
      old_install_name=`otool -D $x | tail -1 | sed -e's|:$||'`
      new_install_name=%{i}/lib/`basename $old_install_name`
      echo $old_install_name", "$new_install_name", "$x
      install_name_tool -id $new_install_name $x
      # Change dependencies hardcoded path to new install path.
      for dep in `otool -L $x | grep "@executable" | grep -v -e':$'`
      do
        newdep=%{i}/lib/`basename $dep`
        echo $dep", "$newdep", "$x
        install_name_tool -change $dep $newdep $x
      done
      chmod -w $x
    fi
done


