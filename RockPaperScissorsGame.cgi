#!/usr/bin/perl
$| = 1;

$method=lc($ENV{'REQUEST_METHOD'});
if($method eq "post"){
  read(STDIN, $qstr, $ENV{'CONTENT_LENGTH'});
}else{
  $qstr = $ENV{'QUERY_STRING'};
  }

$btn = &url_decode($qstr,'btn');
$lastsum = &url_decode($qstr,'lastsum');
$count =  &url_decode($qstr,'count');
$message =  &url_decode($qstr,'message');
$BeforeResult = &url_decode($qstr,'BeforeResult');
$pov = &url_decode($qstr,'pov');
$sumwin =  &url_decode($qstr,'sumwin');
$sumlose =  &url_decode($qstr,'sumlose');
$sumtie =  &url_decode($qstr,'sumtie');
$result =  &url_decode($qstr,'result');
$result2 =  &url_decode($qstr,'result2');

if(($count==0) or ($btn eq "Reset")){
  $message = "じゃんけんゲームの開始です。";
  $lastsum = 0;
  $count = 0;
  $sumwin= 0;
  $sumlose = 0;
  $sumtie = 0;
  $BeforeResult="";
  $pov=0;
}else{
  @item=("@","Y","W");
  $ComputerChoice = $item[int(rand(3))];

  if ((($ComputerChoice eq "@") and( $btn eq "W")) or(($ComputerChoice eq "W") and ($btn eq "Y")) or(($ComputerChoice eq "Y") and( $btn eq "@"))){
    $value =  10;
    $BeforeResult="勝ちました";
    $sumwin = $sumwin+1;
  }elsif ((($ComputerChoice eq "@") and( $btn eq "Y")) or(($ComputerChoice eq "W") and ($btn eq "@")) or(($ComputerChoice eq "Y") and( $btn eq "W"))){
    $value= 0;
    $BeforeResult='まけました';
    $sumlose = $sumlose+1;
  }else{
    $value = 5;
    $BeforeResult="あいこでした";
    $sumtie = $sumtie+1;
  } 
  $message = "第$count回戦:$BeforeResult (自分は$btn、相手は$ComputerChoice)";
  $pov = $sumwin / $count;
  $result = "勝利：$sumwin回  ,  負け：$sumlose回  ,    あいこ:$sumtie回";
  $result2 = "勝率: $pov ";  
}
$count = $count+1;
$lastsum = $lastsum+$value;

print<<EOF;
Content-type: text/html; charset=utf-8

<html>
<head>
<title>じゃんけんゲーム</title>
</head>
<body bgcolor="#333333" text="#EEEEEE">
<p>
$message
</p>
<p>
総得点は$lastsum 点です。

</p>
<p>
<form method="get" action="kadai2b.cgi">

  <input type="hidden" name="lastsum" value=$lastsum>
  <input type="hidden" name="count" value=$count>
  <input type="hidden" name="sumwin" value=$sumwin> 
  <input type="hidden" name="sumlose" value=$sumlose>
  <input type="hidden" name="sumtie" value=$sumtie>
  <input type="submit" name="btn" value="@">
  <input type="submit" name="btn" value="Y">
  <input type="submit" name="btn" value="W">
  <input type="submit" name="btn" value="Reset">

</form>
</p>
<p>
現在までの結果：
$result
  
$result2
</p>

</body>
</html>
EOF

sub url_decode() {
  my @pairs = split(/&/,$_[0]);
  foreach my $pair (@pairs){
    (my $name, my $val)=split(/=/,$pair);
    if($name eq $_[1]){
    $val =~ tr/+/ /;
    $val =~ s/%([0-9A-Fa-f][0-9A-Fa-f])/pack('H2',$1)/eg;
    return $val;
    }
   }
}
