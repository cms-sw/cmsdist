#!/bin/sh -e
#
#TODO: check that versions coincide

rm -f lhapdf6_makeLinks.file
echo "#!/bin/sh -e" > lhapdf6_makeLinks.file
echo >> lhapdf6_makeLinks.file
echo "#PDF sets list is made for:" >> lhapdf6_makeLinks.file
echo "export lhapdf6Version=$1" >> lhapdf6_makeLinks.file
echo >> lhapdf6_makeLinks.file
echo "if [ x%1 != x%lhapdf6Version ]; then" >> lhapdf6_makeLinks.file
echo "  echo lhapdf6_makeLinks: lhapdf6 versions do not coincide" >> lhapdf6_makeLinks.file
echo "  echo please create this script by running hapdf6_makeScript.sh with correct version" >> lhapdf6_makeLinks.file
echo "  exit 1" >> lhapdf6_makeLinks.file
echo "fi" >> lhapdf6_makeLinks.file
echo >> lhapdf6_makeLinks.file
#
echo "export cvmfspath=/cvmfs/cms.cern.ch/lhapdf/pdfsets/%1" >> lhapdf6_makeLinks.file
export ss=`ls /cvmfs/cms.cern.ch/lhapdf/pdfsets/$1`
echo export pdflist=@${ss}@ >> lhapdf6_makeLinks.file
echo "for pdf in %{pdflist} ; do" >> lhapdf6_makeLinks.file 
echo "  if [ ! -d @%{pdf}@ ] ; then" >> lhapdf6_makeLinks.file
echo "    echo missing pdf: %{pdf} ---" >> lhapdf6_makeLinks.file
echo "    echo making soft link to cvmfs" >> lhapdf6_makeLinks.file
echo "    ln -fs %{cvmfspath}/%{pdf} %{pdf}" >> lhapdf6_makeLinks.file
echo "  fi" >> lhapdf6_makeLinks.file
echo "done" >> lhapdf6_makeLinks.file

sed "s/%/$/g" < lhapdf6_makeLinks.file > lhapdf6_makeLinks.file_1
sed "s/@/\"/g" < lhapdf6_makeLinks.file_1 > lhapdf6_makeLinks.file_2
mv lhapdf6_makeLinks.file_2 lhapdf6_makeLinks.file
rm -f lhapdf6_makeLinks.file_*
