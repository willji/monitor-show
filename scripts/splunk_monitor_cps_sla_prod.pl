#!/usr/bin/perl
use strict;
use LWP::UserAgent;
use HTTP::Cookies;
use Data::Dumper;
use POSIX qw(strftime);


my $browser = LWP::UserAgent->new;

$browser->agent('Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/33.0.1750.154 Safari/537.36');
my $cookie_jar=HTTP::Cookies->new(file =>"/tmp/foo",autosave => 1,ignore_discard => 1);
$browser->cookie_jar($cookie_jar);

#my $url_domain = "https://192.168.63.112:8089";
my $url_domain = "https://172.16.50.41:13089";

my $url = "${url_domain}/servicesNS/inf/search/search/jobs/export";
#my $url = "${url_domain}/servicesNS/query/search/search/jobs/export";

my $login_url = "${url_domain}/services/auth/login";
#my $resp = $browser->post("$login_url",["username"=>"query","password"=>"query123",]);
my $resp = $browser->post("$login_url",["username"=>"inf","password"=>"jiagouzu123",]);
#print $resp->content;
my $key;
$key = $1 if $resp->content =~ /<sessionKey>(.+?)<\/sessionKey>/;

$browser->default_header("Authorization","Splunk $key");

my @apps = ("中国银联-CP-专线-00010001","中国银联-CNP-专线-00010100","上海工行借贷记卡快捷-专线-01021100","深圳农行快捷-CNP-专线-01030103");
#my @apps = ();

my $search_hash = {
    "中国银联-CP-专线-00010001" => 'search source="/opt/log/cps/cups/cups.log" ("Qcup send a txn msg to bank" OR "Qcup recived a txn msg from bank") txnReference != "00010001" | transaction trans_id  startswith="Qcup send a txn msg to bank" endswith="Qcup recived a txn msg from bank"|stats avg(duration)  as aging',
    "中国银联-CNP-专线-00010100" => 'search source="/opt/log/app-bgw-cup-sh-cnp/app-bgw-cup-sh-cnp.log" ("Bgw Send To Bank" OR "Bgw From Bank") | transaction merOrderNum  startswith="Bgw Send To Bank" endswith="Bgw From Bank"|stats avg(duration) as aging',
    "上海工行借贷记卡快捷-专线-01021100" => 'search source="/opt/log/cps/bgw-icbc-sh-dc-ep/app-bgw-icbc-sh.dc-ep.log" ("bgw2bank" OR "bank2bgw") | transaction biz_num  startswith="bgw2bank" endswith="bank2bgw"|stats avg(duration) as aging',
    "深圳农行快捷-CNP-专线-01030103" => 'search source="/opt/log/cps/bgw-abc-sz-ep/bgw-abc-sz-ep.log" ("Data from bank" OR "Data Send To Bank") | transaction IdTxnCtrl  startswith="Data Send To Bank" endswith="Data from bank"|stats avg(duration) as aging',
};

while (1) {
my $main_destination_file = "/opt/oracle/apache/htdocs/panoramic/datas/sla.data";
my $output_data;
my $time_str = strftime("%Y-%m-%d %H:%M", localtime(time));
$output_data = "time=$time_str\n";
foreach my $app (@apps) {
print $app."\n";
$output_data .= "[$app]\n";
my $search_string = $search_hash->{$app};
$resp = $browser->post($url,["search"=>$search_string,"output_mode"=>"csv","earliest_time"=>"-10m","latest_time"=>"now",]);
#print $resp->content;

my $content = $resp->content;
$content =~ s/\"//g;
my @array = split /\n/,$content;
my @fields_array = split /,/,$array[0];
#die Dumper @fields_array;


my $data_hash;
if (defined $fields_array[0]) {
	my $hash;
	for (0..$#fields_array) {
		$hash->{$fields_array[$_]} = $_;
	}
    for (1..$#array) {
        $output_data .= "time=".(round($array[$_]*100)/100)."\n";
    }
}
else {
	$output_data .= "time=N/A\n";
	print "Currenly no trade\n";
}
}

my @db_app = ("mas","aps");

for my $db_app (@db_app) {
	$output_data .= "[$db_app]\n";
	my $arr = get_data_by_app($db_app);
	foreach my $str (@$arr) {
		$output_data .= "$str\n";	
	}
	print Dumper $arr;
#	die $db_app;
}
#die $output_data."\n";
open FILE,">$main_destination_file" or die $!;
        print FILE $output_data;
        close FILE;
sleep 180;
}

sub round {
        my ($num) = @_;

        return int($num+0.5);
}

sub get_data_by_app {
	my ($app) = @_;

	my $browser = LWP::UserAgent->new;
	$browser->agent('Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/33.0.1750.154 Safari/537.36');
	$browser->cookie_jar({});
        $browser->get('https://query.99bill.com/report/login.do?userid=roman.xu@99bill.com&passwd=roma23499');
	my $url = "https://query.99bill.com/report/result.do";
	$browser->default_header("referer","https://query.99bill.com/report/blankresult.jsp");
	my $resp;
	if ($app eq "mas") {
		$resp = $browser->post($url,["id" => "sqlSearch","category" => "vposdgl", "searchSql" => "&thesql=select * from (
select sourceid ID,round((timeout/total),4)*100||'%' RATE
from(
select substr(tunnel_data,instr(tunnel_data, 'mas.source.id', 1, 1) + 16,6) sourceid,
       count(1) total,
       sum(case when trunc(extract(second from resp_time - txn_time), 2) > 5 then 1 else 0 end) timeout
    from maspos.t_txn_ctrl t
   where  txn_time> sysdate - 10/1440
and txn_type = '00200'
     and resp_time is not null
   group by substr(tunnel_data,
                   instr(tunnel_data, 'mas.source.id', 1, 1) + 16,
                   6)
)order by round((timeout/total),4)*100 desc
)where rownum<4",]);
	}
	elsif ($app eq "aps") {
		$resp = $browser->post($url,["id" => "sqlSearch","category" => "vposdgl", "searchSql" => "&thesql=select * from (
select sourceid ID,round((timeout/total),4)*100||'%' RATE
from(
select substr(tunnel_data,
                instr(tunnel_data, 'aps.sourceId', 1, 1) + 15,
                6) sourceid,
       count(1) total,
       sum(case when trunc(extract(second from resp_time - txn_time), 2) > 5 then 1 else 0 end) timeout
    from maspos.t_txn_ctrl t
   where  txn_time> sysdate - 10/1440
and txn_type = '00200'
     and resp_time is not null
and SRV_CHAN_TYPE!='B'
and auth_net_id!='99BL0000'
   group by substr(tunnel_data,
                instr(tunnel_data, 'aps.sourceId', 1, 1) + 15,
                6)
)order by round((timeout/total),4)*100 desc
)where rownum<4",]);
	}
	else {
		return undef;
	}
	my @arr;
	my $content = $resp->content;
	while ($content =~ m{<tr onclick='heighlight\(event\)'><td style='text-align:left'>([^<]+?)</td><td style='text-align:left'>([^<]+?)</td></tr>}g) {
		my $str = "$1=$2";
		push @arr,$str;
	}

	return \@arr;
}
