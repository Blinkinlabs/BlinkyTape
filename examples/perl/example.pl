#!/usr/bin/env perl
#
# If you are on Mac OS X do consider installing Perlbrew from http://perlbrew.pl/,
# then the latest stable Perl and cpanm using it.
#
# Install Device::BlinkyTape from CPAN
#

use Device::BlinkyTape::WS2811; # BlinkyTape uses WS2811

# Simulation requires the Perl module Tk to be installed.
# Install it from CPAN.
# It will display the BlinkyTape on your screen so that
# you can develop before actually getting the device.
#
my $bb = Device::BlinkyTape::WS2811->new(simulate => 1);

$bb->all_on();
sleep 2;
$bb->all_off();
sleep 2;
$bb->send_pixel(255,255,255);
$bb->show();
sleep 2;
$bb->send_pixel(255,0,0);
$bb->show();
sleep 2;
$bb->send_pixel(240,0,0);
$bb->show();
sleep 2;

# Go crazy
for (my $b=0; $b<=1000; $b++) {
    for (my $a=0; $a<=59; $a++) {
        $bb->send_pixel(int(rand(254)),int(rand(254)),int(rand(254)));
    }
    $bb->show(); # shows the sent pixel row
}
sleep 2;
