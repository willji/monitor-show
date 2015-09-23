#!/usr/bin/perl
use strict;
use LWP::UserAgent;
use HTTP::Cookies;
use Data::Dumper;
use POSIX qw(strftime);

#my $tomcat_path = "/opt/monitor/ROOT/cps";
#my $root_path = "/opt/monitor/monitor_cps/txn";
my $tomcat_path = "/tmp/";
my $root_path = "/nfs/monitor_cps/txn";

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

my @apps = ("中国银联-CP-专线-00010001","中国银联-CNP-专线-00010100","中国银联2.1快捷-专线-00012100","上海工行借贷记卡快捷-专线-01021100","深圳农行快捷-CNP-专线-01030103");

my $search_hash = {
    "中国银联-CP-专线-00010001" => 'search source="/opt/log/cps/cups/cups.log" "Qcup send a txn msg to bank" |stats count as request by host|appendcols [search source="/opt/log/cps/cups/cups.log" "Qcup recived a txn msg from bank" |stats count as response by host]',
    "中国银联-CNP-专线-00010100" => 'search source="/opt/log/app-bgw-cup-sh-cnp/app-bgw-cup-sh-cnp.log" "Bgw Send To Bank" |stats count as request by host|appendcols [search source="/opt/log/app-bgw-cup-sh-cnp/app-bgw-cup-sh-cnp.log" "Bgw From Bank" |stats count as response by host]',
    "中国银联2.1快捷-专线-00012100" => 'search source="/opt/log/app-bgw-cup-qg-ep/app-bgw-cup-qg-ep.log" "request body:[bgw2bank|start" | stats count as request by host| appendcols [search source="/opt/log/app-bgw-cup-qg-ep/app-bgw-cup-qg-ep.log" "cup.qg.ep bank responseCode" |stats count as response by host]',
    "上海工行借贷记卡快捷-专线-01021100" => 'search source="/opt/log/cps/bgw-icbc-sh-dc-ep/app-bgw-icbc-sh.dc-ep.log" "bgw2bank" | stats count as request by host| appendcols [search source="/opt/log/cps/bgw-icbc-sh-dc-ep/app-bgw-icbc-sh.dc-ep.log" "bank2bgw" |stats count as response by host]',
    "深圳农行快捷-CNP-专线-01030103" => 'search source="/opt/log/cps/bgw-abc-sz-ep/bgw-abc-sz-ep.log" "Data Send To Bank" | stats count as request by host| appendcols [search source="/opt/log/cps/bgw-abc-sz-ep/bgw-abc-sz-ep.log" "Data from bank" |stats count as response by host]',
};


while (1) {
my $main_destination_file = "/opt/oracle/apache/htdocs/panoramic/datas/bgw.data";
my $output_data;
my $time_str = strftime("%Y-%m-%d %H:%M", localtime(time()-60));
$output_data = "time=$time_str\n";
foreach my $app (@apps) {
print $app."\n";
$output_data .= "[$app]\n";
my $search_string = $search_hash->{$app};
$resp = $browser->post($url,["search"=>$search_string,"output_mode"=>"csv","earliest_time"=>'-1m@m',"latest_time"=>'@m',]);
#print $resp->content;

my $content = $resp->content;
$content =~ s/\"//g;
my @array = split /\n/,$content;
my @fields_array = split /,/,$array[0];
#die Dumper @fields_array;


my $data_hash;
if ($#fields_array >= 1) {
	my $hash;
	for (0..$#fields_array) {
		$hash->{$fields_array[$_]} = $_;
	}
    for (1..$#array) {
        my @temp_array = split /,/,$array[$_];
        $output_data .= "$temp_array[$hash->{host}]=$temp_array[$hash->{request}]:$temp_array[$hash->{response}]\n";
    }
}
else {
	print "Cannot get data from splunk\n";
    #print Dumper @fields_array;
}
}
#die $output_data."\n";
open FILE,">$main_destination_file" or die $!;
        print FILE $output_data;
        close FILE;
sleep 30;
}

