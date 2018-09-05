<?php
$domain=$_GET["domain"];
$useBase64=$_GET["base64"];
if('1'==$useBase64){
        $domain = base64_decode($domain);
}

$iparr = dns_get_record($domain,DNS_A);
$info=array(
        domain=>$domain,
        dns=>$iparr,
);
echo json_encode($info);
?>
