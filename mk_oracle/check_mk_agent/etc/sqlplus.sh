#!/bin/sh
# +------------------------------------------------------------------+
# |             ____ _               _        __  __ _  __           |
# |            / ___| |__   ___  ___| | __   |  \/  | |/ /           |
# |           | |   | '_ \ / _ \/ __| |/ /   | |\/| | ' /            |
# |           | |___| | | |  __/ (__|   <    | |  | | . \            |
# |            \____|_| |_|\___|\___|_|\_\___|_|  |_|_|\_\           |
# |                                                                  |
# | Copyright Mathias Kettner 2013             mk@mathias-kettner.de |
# +------------------------------------------------------------------+
#
# This file is part of Check_MK.
# The official homepage is at http://mathias-kettner.de/check_mk.
#
# check_mk is free software;  you can redistribute it and/or modify it
# under the  terms of the  GNU General Public License  as published by
# the Free Software Foundation in version 2.  check_mk is  distributed
# in the hope that it will be useful, but WITHOUT ANY WARRANTY;  with-
# out even the implied warranty of  MERCHANTABILITY  or  FITNESS FOR A
# PARTICULAR PURPOSE. See the  GNU General Public License for more de-
# ails.  You should have  received  a copy of the  GNU  General Public
# License along with GNU Make; see the file  COPYING.  If  not,  write
# to the Free Software Foundation, Inc., 51 Franklin St,  Fifth Floor,
# Boston, MA 02110-1301 USA.

# support for clusterware and connect as sysdba added by:
# Thorsten Bruhns <thorsten.bruhns@opitz-consulting.com>
#
# How to create the wallet?
# mkstore -wrl /etc/check_mk/oracle_wallet -create
# mkstore -wrl /etc/check_mk/oracle_wallet --createEntry trac1 dbsnmp dbsnmp

# EXAMPLE

# This script is called by the Check_MK ORACLE plugin in order to 
# execute an SQL query. 

# It is your task to adapt this script so that the ORACLE environment
# is setup and the correct user chosen to execute sqlplus.

# The script will get the query on stdin and shall output the
# result on stdout. Error messages goes to stderr.

ORACLE_SID=$1
if [ -z "$ORACLE_SID" ] ; then
    echo "Usage: $0 ORACLE_SID" >&2
    exit 1
fi

# sysdbaconnect is needed for physical Standby Databases!
sysdbaconnect=""
sysdbaconnect=" as sysdba"

ORATAB=/etc/oratab
ORACLE_HOME=$(cat ${ORATAB} | grep "^"${ORACLE_SID}":" | cut -d":" -f2)

export TNS_ADMIN=/etc/check_mk

test -f ${TNS_ADMIN}/sqlnet.ora 
if [ ${?} -ne 0 ]
then
	echo "ORA-99998 Couldn't find "${TNS_ADMIN}/sqlnet.ora
	exit 1
fi

# Check for an existing tnsnames.ora
# yes => Use an alias for connecting to the database
# no  => Use EZCONNECT-Syntax with localhost/<ORACLE_SID>
# This is needed in environment where localhost couldn't be used for connecting
# to Oracle.

if [ -f ${TNS_ADMIN}/tnsnames.ora ]
then
	connectstring=${ORACLE_SID}
	${ORACLE_HOME}/bin/tnsping ${ORACLE_SID} > /dev/null 2>&1 
	if [ ${?} -ne 0 ]
	then
		# tnsping not possible
		# => Connect to Oracle won't work!
		echo "ORA-99999 tnsping failed for "${ORACLE_SID}
		exit 1
	fi
else
	# EZCONNECT
	connectstring="localhost/"${ORACLE_SID}
fi

SQLPLUS=${ORACLE_HOME}/bin/sqlplus
if [ ! -x ${SQLPLUS} ]
then
        echo "sqlplus not found or ORACLE_HOME wrong! "
        echo "SQLPLUS="${SQLPLUS}
        exit 1
fi

export ORACLE_HOME
export ORACLE_SID

${SQLPLUS} -L -s /@${connectstring}${sysdbaconnect}

