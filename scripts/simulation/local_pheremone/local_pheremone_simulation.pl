#!/usr/bin/perl
use lib "$ENV{GAMS_ROOT}/scripts/simulation";
use simulation;

$gams_root = $ENV{GAMS_ROOT};
$time = 3600;
$madara_debug = 0;
$gams_debug = 5;
$period = 1;
$num = 10;
$sim = "local_pheremone";
$area = "small";
$plants = "search_area.1";

simulation::run($num, $time, $period, $sim, $area, $madara_debug, $gams_debug, $plants);
