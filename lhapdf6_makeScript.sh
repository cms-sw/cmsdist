#TODO: check hat versions coincide

rm -f lhapdf6_makeLinks.file
echo "#!/bin/sh -e" > lhapdf6_makeLinks.file
echo >> lhapdf6_makeLinks.file
echo "#PDF sets list is made for:" >> lhapdf6_makeLinks.file
echo "#lhapdf6Version = $1" >> lhapdf6_makeLinks.file
echo >> lhapdf6_makeLinks.file
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

sed "s/%/$/" < lhapdf6_makeLinks.file > lhapdf6_makeLinks.file_1
sed "s/%/$/" < lhapdf6_makeLinks.file_1 > lhapdf6_makeLinks.file_2
sed "s/%/$/" < lhapdf6_makeLinks.file_2 > lhapdf6_makeLinks.file_3
sed "s/@/\"/" < lhapdf6_makeLinks.file_3 > lhapdf6_makeLinks.file_4
sed "s/@/\"/" < lhapdf6_makeLinks.file_4 > lhapdf6_makeLinks.file_5
mv lhapdf6_makeLinks.file_5 lhapdf6_makeLinks.file
rm -f lhapdf6_makeLinks.file_*
