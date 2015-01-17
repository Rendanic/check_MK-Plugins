#!/bin/bash
#
# extracts data from Check_MK Package to current directory


pkgname=$1


extract_package() {
	packagename=$(tar -xOzf $pkgname info | grep "'name'" | cut -d"'" -f4)
	export packagename
}

extract_data() {

	for archiv in $(tar -tf $pkgname *.tar )
	do
		echo "extracting "$archiv

		subdir=$(echo $archiv | cut -d"." -f1)
		if [ ! -d $subdir ] ; then
			mkdir $subdir
		fi

		tar -xOzf $pkgname $archiv | tar -C $subdir -xf -
		#extract_subarchiv ${archiv}
	done

}

if [ ! -f "$pkgname" ] ; then
	echo "File "$pkgname" not found!"
	exit 1
fi

echo "Working on "$pkgname
extract_package
extract_data

