use uni::perl;
use strict;
use warnings;

my %re=(
  qr/[A-ZА-ЯЁ]/ => ["A".."Z"],
  qr/[a-zа-яё]/ => ["a".."z"],
  qr/[\d]/ => [0..9],
);
my ($sep, @u)=("\t");
while(<>) {
  chomp;
  my @cols = split qr{$sep};
  for my $c(0..$#cols) {
    my $on=$cols[$c];
    if (!$u[$c]{$on}) {
      my $xn = $on;
      while(my($k,$v) = each(%re)) {
        $xn=~s{$k}{@$v[rand()*$#$v]}sge;
      }
      $u[$c]{$on}=$xn;
    }
    print $c?$sep:'', $u[$c]{$on};
  }
  print $/;
}
