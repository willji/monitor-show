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

my @apps = ("pos_machine","vpos","posp","mgw","internal","mbp","tais","mas","aps");

my $search_hash = {
        "pos_machine" => 'search source=/opt/log/cps/posp/app-posp.log response txnType=00201|stats count by host|eval a=1|eval b=2|fields host count a b',
        "posp" => 'search source="/opt/log/app-posp/app-posp.log" type="I0" OR type="O1"|stats last(date_hour) as hour, last(date_minute) as minute, count(eval(type="I0")) as request,count(eval(type="O1")) as response by host|eval time = hour +":" + minute|fields host, time, request, response',
        "mgw" => 'search source="/opt/log/cps/mgw/app-mgw.log" (txn_type="txn tr1" OR txn_type2="txn query qr1" OR txn_type="txn tr2" OR txn_type2="txn query qr2" OR txn_type1="TR3")|eval tr1=if(txn_type="txn tr1" OR txn_type2="txn query qr1",1,0)|eval tr2=if(txn_type="txn tr2" OR txn_type2="txn query qr2",1,0)|eval tr3=if(txn_type1="TR3",1,0)|stats last(date_hour) as hour last(date_minute) as minute sum(tr1) as tr1 sum(tr2) as tr2 sum(tr3) as tr3 by host|eval time = hour + ":" + minute|fields host time tr1 tr2 tr3',
        "internal" => 'search source="/opt/log/app-internal/app-internal.log" (operation="process seashell request Begin" OR operation="process seashell request End") | eval request=if(operation="process seashell request Begin",1,0)|eval response=if(operation="process seashell request End",1,0)|stats last(date_hour) as hour last(date_minute) as minute sum(request) as request sum(response) as response by host|eval time = hour + ":" + minute|fields host time request response',
        "vpos" => 'search  source="/opt/log/cps/vpos/app-vpos.log" (operation="Begin 1" OR operation="End 1") | eval request=if(operation="Begin 1",1,0)|eval response=if(operation="End 1",1,0)|stats last(date_hour) as hour last(date_minute) as minute sum(request) as request sum(response) as response by host|eval time = hour + ":" + minute|fields host time request response',
        "tais" => 'search  source="/opt/log/app-tais/app-tais.log" (operation="Start mainTxn" OR operation="Send to channel" OR operation="Tais txn Forward") | eval request=if(operation="Start mainTxn",1,0)|eval response=if(operation="Send to channel",1,0)|eval forward=if(operation="Tais txn Forward",1,0)|stats last(date_hour) as hour last(date_minute) as minute sum(request) as request sum(response) as response sum(forward) as forward by host|eval time = hour + ":" + minute|fields host time request response forward',
        "mas" => 'search source="/opt/log/app-mas/app-mas.log" (operation="receive client request" OR operation="response sended to service channel") | eval request=if(operation="receive client request",1,0)|eval response=if(operation="response sended to service channel",1,0)|stats last(date_hour) as hour last(date_minute) as minute sum(request) as request sum(response) as response by host|eval time = hour + ":" + minute|fields host time request response',
        "aps" => 'search source="/opt/log/app-aps/app-aps.log" "Send message to bgw queue" OR "Receive bgw message" OR "ep recvMessage idTxnCtrl"| eval result=if(operation=="Send message to bgw queue",1,0) | stats last(date_hour) as hour, last(date_minute) as minute, count(eval(result=1)) as request,count(eval(result=0)) as response by host|eval time = hour +":" + minute|fields host, time, request, response',
        "mbp" => 'search source="/opt/log/cps/mbp/CPS.app-mbp.log" (operation="send sms success" OR operation="receive saf message") | eval request=if(operation="send sms success",1,0)|eval response=if(operation="receive saf message",1,0)|stats last(date_hour) as hour last(date_minute) as minute sum(request) as request sum(response) as response by host|eval time = hour + ":" + minute|fields host time request response',
};

#my $app = "posp";
#my $group = "T";
my @groups = ("T","A","B");

while (1) {
my $main_destination_file = "/opt/oracle/apache/htdocs/panoramic/datas/splunk.data";
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
if ($#fields_array >= 3) {
	my $hash;
	for (0..$#fields_array) {
		$hash->{$fields_array[$_]} = $_;
	}
	for (1..$#array) {
		my @temp_array = split /,/,$array[$_];
		#$data_hash->{$temp_array[$hash->{"host"}]}->{"time"} = $temp_array[$hash->{"time"}];
		if ($app eq "mgw") {
			$data_hash->{$temp_array[$hash->{"host"}]}->{"tr1"} = $temp_array[$hash->{"tr1"}];
			$data_hash->{$temp_array[$hash->{"host"}]}->{"tr2"} = $temp_array[$hash->{"tr2"}];
			$data_hash->{$temp_array[$hash->{"host"}]}->{"tr3"} = $temp_array[$hash->{"tr3"}];
            $output_data .= "$temp_array[$hash->{host}]=$temp_array[$hash->{tr1}]:$temp_array[$hash->{tr2}]\n";
		}
        elsif ($app eq "pos_machine") {
            $data_hash->{$temp_array[$hash->{"host"}]}->{"count"} = $temp_array[$hash->{"count"}];
            $output_data .= "$temp_array[$hash->{host}]=$temp_array[$hash->{count}]\n";
        }
		elsif ($app eq "tais") {
			$data_hash->{$temp_array[$hash->{"host"}]}->{"request"} = $temp_array[$hash->{"request"}];
                        $data_hash->{$temp_array[$hash->{"host"}]}->{"resp"} = $temp_array[$hash->{"response"}];
			$data_hash->{$temp_array[$hash->{"host"}]}->{"forward"} = $temp_array[$hash->{"forward"}];
            $output_data .= "$temp_array[$hash->{host}]=$temp_array[$hash->{request}]:$temp_array[$hash->{response}]:$temp_array[$hash->{forward}]\n";
		}
		else {
			$data_hash->{$temp_array[$hash->{"host"}]}->{"request"} = $temp_array[$hash->{"request"}];
			$data_hash->{$temp_array[$hash->{"host"}]}->{"resp"} = $temp_array[$hash->{"response"}];
            $output_data .= "$temp_array[$hash->{host}]=$temp_array[$hash->{request}]:$temp_array[$hash->{response}]\n";
		}
	}
      
}
else {
	print "Cannot get data from splunk\n";
    #print Dumper @fields_array;
}
}
open FILE,">$main_destination_file" or die $!;
        print FILE $output_data;
        close FILE;
sleep 30;
}

