Packages for Check_MK

Homepage of Check_MK: http://mathias-kettner.de/check_mk.html

# mk_oracle
This plugin was redesigned in cooperation between Mathias Kettner
and Thorsten Bruhns. mk_oracle use the new run_cached in this plugin
which makes the future development much easier then before.
The master branch of this repository need Check_MK 1.2.6 or newer due
to a change in the internal API of Check_MK. The backporting for 1.2.2
has been stoped and moved to the 1.2.2 branch. I also moved the 
Changelog of mk_oracle to an own file.

## Requirements
* Linux   RDBMS 9.2, 10.2, 11.1, 11.2, XE 11.2, 12.1
* AIX 5.3 RDBMS 11.2
* ASM: 10.2, 11.1, 11.2, 12.1 
* Check_MK Agent 1.2.2p2 or newer

## Documentation
The documentation is availible at the Homepage of Check_MK:
https://mathias-kettner.de/checkmk_oracle.html


# mk_oracle_crs
This plugin is used to check an Oracle Grid-Infrastructure or Oracle Restart.

## Requirements
* Linux   Grid-Infrastructure or Oracle Restart 11.2 + 12.1, Oracle CRS 10.2 + 11.1
* Check_MK Agent 1.2.2p2 or newer

## Version History
* 2015.01.16.1.2.2p0_tbr: Plugin compatibility against CRS 10.2 and 11.1
* 2014.11.06.1.2.2p0_tbr: fix for Pending Services in CRS or GI Environments
* 2014.09.28_1.2.2p0_tbr: Support for Gird-Infrastructure 12.1 added
* 2014.09.28_1.2.2p0_tbr: Support for Gird-Infrastructure 12.1 added

* 2014.08.29_1.2.2p0_tbr: ae03fa3 Fixed shell expansion and lower problem in mk_oracle_crs

* 0.1.0: 1st release on github

## Local Checks
# plugin_cksum

Calculates a checksum with cksum over all plugins which are found in $MK_LIBDIR/plugins.
The state is OK when plugins are found and UNKNOWN when the directory or cksum is missing.
Thorsten Bruhns
