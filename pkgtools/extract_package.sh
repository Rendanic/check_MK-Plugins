#!/bin/bash
#
# extracts data from Check_MK Package to current directory


tmpdir=/tmp
pkgname=$PWD/$1

pwd=$PWD

extract_package() {
	oldpwd=$PWD
	cd /tmp
	tar -xzf $pkgname info
	packagename=$(grep "'name'" /tmp/info | cut -d"'" -f4)
	export packagename
	
	tmppkgdir=/tmp/$packagename
	test -d $tmppkgdir || mkdir $tmppkgdir
	cd $tmppkgdir
	tar -xzf $pkgname 
	cd $oldpwd
}

extract_subarchiv() {
	archivetype=$1
	tarfile=$tmppkgdir/${archivetype}.tar

	if [ -f ${tarfilee} ]
	then
		cd $pwd/$packagename
		test -d $archivetype || mkdir $archivetype
		cd $archivetype
		tar -xf $tmppkgdir/${archivetype}.tar
	fi
	
}

extract_data() {
	tmppkgdir=/tmp/$packagename

	cd $pwd
	test -d $packagename || mkdir $packagename
	cd $packagename
	for archiv in $(cd /tmp/${packagename}/ ; ls *tar | cut -d"." -f1)
	do
		extract_subarchiv ${archiv}
	done

}

extract_package
echo "Working on "$packagename
extract_data

