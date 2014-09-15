<?php
# +------------------------------------------------------------------+
# |             ____ _               _        __  __ _  __           |
# |            / ___| |__   ___  ___| | __   |  \/  | |/ /           |
# |           | |   | '_ \ / _ \/ __| |/ /   | |\/| | ' /            |
# |           | |___| | | |  __/ (__|   <    | |  | | . \            |
# |            \____|_| |_|\___|\___|_|\_\___|_|  |_|_|\_\           |
# |                                                                  |
# | Copyright Mathias Kettner 2014             mk@mathias-kettner.de |
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

$title = str_replace("_", " ", $servicedesc);
$opt[1] = "--vertical-label 'Time(s)' -X0 --upper-limit " . ($MAX[1] * 120 / 100) . " -l0  --title \"Database Time $hostname / $title\" ";

# For the rest of the data we rather work with names instead
# of numbers
$RRD = array();
foreach ($NAME as $i => $n) {
    $RRD[$n] = "$RRDFILE[$i]:$DS[$i]:MAX";
    $WARN[$n] = $WARN[$i];
    $CRIT[$n] = $CRIT[$i];
    $MIN[$n]  = $MIN[$i];
    $MAX[$n]  = $MAX[$i];
}

$def[1] = "";

if (isset($RRD['DB_time'])) {
   $def[1] .= "DEF:DB_time=$RRD[DB_time] "
           . "GPRINT:DB_time:LAST:\"%6.0lf s last\" "
           . "GPRINT:DB_time:AVERAGE:\"%6.0lf s avg\" "
           . "GPRINT:DB_time:MAX:\"%6.0lf s max\\n\" " 
           . "AREA:DB_time#008030:\"DB Time        \" "
        . "'COMMENT:\\n' ";
}

if (isset($RRD['DB_CPU'])) {
   $def[1] .= "DEF:DB_CPU=$RRD[DB_CPU] "
           . "AREA:DB_CPU#80ff40:\"DB CPU        \" "
           . "GPRINT:DB_CPU:LAST:\"%6.0lf s last\" "
           . "GPRINT:DB_CPU:AVERAGE:\"%6.0lf s avg\" "
           . "GPRINT:DB_CPU:MAX:\"%6.0lf s max\\n\" " ;
}

$opt[2] = "--vertical-label 'percentage' -X0 --upper-limit " . ($MAX[1] * 120 / 100) . " -l0  --title \"Database Time $hostname / $title\" ";
$def[2] = "";
if (isset($RRD['buffer_hit_ratio'])) {
   $def[2] .= "DEF:buffer_hit_ratio=$RRD[buffer_hit_ratio] "
           . "LINE2:buffer_hit_ratio#80ff40:\"Buffer Cache Hit Ratio   \" "
           . "GPRINT:buffer_hit_ratio:LAST:\"%6.0lf  last\" "
           . "GPRINT:buffer_hit_ratio:AVERAGE:\"%6.0lf  avg\" "
           . "GPRINT:buffer_hit_ratio:MAX:\"%6.0lf  max\\n\" " ;
}

$opt[3] = "--vertical-label 'percentage' -X0 --upper-limit " . ($MAX[1] * 120 / 100) . " -l0  --title \"Database Time $hostname / $title\" ";
$def[3] = "";
if (isset($RRD['library_cache_hit_ratio'])) {
   $def[3] .= "DEF:library_cache_hit_ratio=$RRD[library_cache_hit_ratio] "
           . "LINE2:library_cache_hit_ratio#80ff40:\"Buffer Cache Hit Ratio   \" "
           . "GPRINT:library_cache_hit_ratio:LAST:\"%6.0lf  last\" "
           . "GPRINT:library_cache_hit_ratio:AVERAGE:\"%6.0lf  avg\" "
           . "GPRINT:library_cache_hit_ratio:MAX:\"%6.0lf  max\\n\" " ;
}

$opt[4] = "--vertical-label 'Counts' -X0 --upper-limit " . ($MAX[1] * 120 / 100) . " -l0  --title \"Database Time $hostname / $title\" ";
$def[4] = "";
if (isset($RRD['consistent_gets'])) {
   $def[4] .= "DEF:consistent_gets=$RRD[consistent_gets] "
           . "LINE1:consistent_gets#80ff40:\"Consistent Gets  \" "
           . "GPRINT:consistent_gets:LAST:\"%6.0lf  last\" "
           . "GPRINT:consistent_gets:AVERAGE:\"%6.0lf  avg\" "
           . "GPRINT:consistent_gets:MAX:\"%6.0lf  max\\n\" " ;
}

if (isset($RRD['physical_reads'])) {
   $def[4] .= "DEF:physical_reads=$RRD[physical_reads] "
           . "LINE1:physical_reads#008030:\"Physical Reads \" "
           . "GPRINT:physical_reads:LAST:\"%6.0lf  last\" "
           . "GPRINT:physical_reads:AVERAGE:\"%6.0lf  avg\" "
           . "GPRINT:physical_reads:MAX:\"%6.0lf  max\\n\" " ;
}
