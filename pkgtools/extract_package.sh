#!/bin/bash

tmpdir=/tmp
pkgname=$PWD/$1

pwd=$PWD

extract_package() {
	oldpwd=$PWD
	cd /tmp
	tar -xvzf $pkgname info
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
	cd $pwd/$packagename
	test -d $archivetype || mkdir $archivetype
	cd $archivetype
	tar -xf $tmppkgdir/${archivetype}.tar
	
}

extract_data() {
	tmppkgdir=/tmp/$packagename

	cd $pwd
	test -d $packagename || mkdir $packagename
	cd $packagename

	extract_subarchiv agents
	extract_subarchiv checks
	extract_subarchiv pnp-templates
	extract_subarchiv web

}

extract_package
extract_data
echo $packagename

