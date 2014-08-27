<?php
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
$i=0;

$RRD = array();
foreach ($NAME as $i => $n) {
    $RRD[$n] = "$RRDFILE[$i]:$DS[$i]:MAX";
    $WARN[$n] = $WARN[$i];
    $CRIT[$n] = $CRIT[$i];
    $MIN[$n]  = $MIN[$i];
    $MAX[$n]  = $MAX[$i];
    $ACT[$n]  = $ACT[$i];
}

$i++;

$title = str_replace("_", " ", $servicedesc);
$opt[$i] = "--vertical-label 'DB CPU/s' -l0  --title \"DB Time/s for $hostname / $title\" ";

$def[$i] = "DEF:DB_time=$RRDFILE[1]:$DS[1]:MAX ";
$def[$i] .= "AREA:DB_time#00ff48: ";
$def[$i] .= "LINE:DB_time#008f38: ";
$def[$i] .= "GPRINT:DB_time:LAST:\"last\: %3.0lf\" ";
$def[$i] .= "GPRINT:DB_time:AVERAGE:\"avg\: %3.0lf\" ";
$def[$i] .= "GPRINT:DB_time:MAX:\"max\: %3.0lf\" ";


$i++;
$opt[$i] = "--vertical-label 'DB CPU/s' -l0  --title \"DB CPU/s for $hostname / $title\" ";

$def[$i] = "DEF:DB_CPU=$RRDFILE[2]:$DS[2]:MAX ";
$def[$i] .= "AREA:DB_CPU#00ff48: ";
$def[$i] .= "LINE:DB_CPU#008f38: ";
$def[$i] .= "GPRINT:DB_CPU:LAST:\"last\: %3.0lf\" ";
$def[$i] .= "GPRINT:DB_CPU:AVERAGE:\"avg\: %3.0lf\" ";
$def[$i] .= "GPRINT:DB_CPU:MAX:\"max\: %3.0lf\" ";

$i++;
if (isset($RRD["library_cache_hit_ratio"])) {
    $def[$i]     = "";
    $opt[$i] = "--vertical-label 'Ratio in %' -l0  --title \"Library Cache Hit Ratio for $hostname / $title\" ";
        $ds_name[$i] = "Requests/sec";
    $color = '#000000';
    foreach ($this->DS as $KEY=>$VAL) {
        if($VAL['NAME'] == 'library_cache_hit_ratio') {
            $def[$i]    .= rrd::def     ("var".$KEY, $VAL['RRDFILE'], $VAL['DS'], "AVERAGE");
            $def[$i]    .= rrd::line1   ("var".$KEY, $color, rrd::cut($VAL['NAME'],16), 'STACK' );
            $def[$i]    .= rrd::gprint  ("var".$KEY, array("LAST","MAX","AVERAGE"), "%6.1lf/s");
        }
    }
}

$i++;
if (isset($RRD["buffer_hit_ratio"])) {
    $def[$i]     = "";
    $opt[$i] = "--vertical-label 'Ratio in %' -l0  --title \"Buffer Cache Hit Ratio for $hostname / $title\" ";
        $ds_name[$i] = "Requests/sec";
    $color = '#000000';
    foreach ($this->DS as $KEY=>$VAL) {
        if($VAL['NAME'] == 'buffer_hit_ratio') {
            $def[$i]    .= rrd::def     ("var".$KEY, $VAL['RRDFILE'], $VAL['DS'], "AVERAGE");
            $def[$i]    .= rrd::line1   ("var".$KEY, $color, rrd::cut($VAL['NAME'],16), 'STACK' );
            $def[$i]    .= rrd::gprint  ("var".$KEY, array("LAST","MAX","AVERAGE"), "%6.1lf/s");
        }
    }
}

$i++;
if (isset($RRD["consistent_gets"])) {
    $def[$i]     = "";
    $opt[$i] = "--vertical-label 'Ratio in %' -l0  --title \"Consistent Gets for $hostname / $title\" ";
        $ds_name[$i] = "Requests/sec";
    $color = '#000000';
    foreach ($this->DS as $KEY=>$VAL) {
        if($VAL['NAME'] == 'consistent_gets') {
            $def[$i]    .= rrd::def     ("var".$KEY, $VAL['RRDFILE'], $VAL['DS'], "AVERAGE");
            $def[$i]    .= rrd::line1   ("var".$KEY, $color, rrd::cut($VAL['NAME'],16), 'STACK' );
            $def[$i]    .= rrd::gprint  ("var".$KEY, array("LAST","MAX","AVERAGE"), "%6.1lf/s");
        }
    }
}

$i++;
if (isset($RRD["physical_reads"])) {
    $def[$i]     = "";
    $opt[$i] = "--vertical-label 'Ratio in %' -l0  --title \"Physical Reads for $hostname / $title\" ";
        $ds_name[$i] = "Requests/sec";
    $color = '#000000';
    foreach ($this->DS as $KEY=>$VAL) {
        if($VAL['NAME'] == 'physical_reads') {
            $def[$i]    .= rrd::def     ("var".$KEY, $VAL['RRDFILE'], $VAL['DS'], "AVERAGE");
            $def[$i]    .= rrd::line1   ("var".$KEY, $color, rrd::cut($VAL['NAME'],16), 'STACK' );
            $def[$i]    .= rrd::gprint  ("var".$KEY, array("LAST","MAX","AVERAGE"), "%6.1lf/s");
        }
    }
}

$i++;
if (isset($RRD["db_block_gets"])) {
    $def[$i]     = "";
    $opt[$i] = "--vertical-label 'Ratio in %' -l0  --title \"Physical Reads for $hostname / $title\" ";
        $ds_name[$i] = "Requests/sec";
    $color = '#000000';
    foreach ($this->DS as $KEY=>$VAL) {
        if($VAL['NAME'] == 'db_block_gets') {
            $def[$i]    .= rrd::def     ("var".$KEY, $VAL['RRDFILE'], $VAL['DS'], "AVERAGE");
            $def[$i]    .= rrd::line1   ("var".$KEY, $color, rrd::cut($VAL['NAME'],16), 'STACK' );
            $def[$i]    .= rrd::gprint  ("var".$KEY, array("LAST","MAX","AVERAGE"), "%6.1lf/s");
        }
    }
}
