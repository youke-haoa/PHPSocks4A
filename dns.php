<?php
$domain=$_GET["domain"];
$iparr = dns_get_record($domain,DNS_A);
$info=array(
        domain=>$domain,
        dns=>$iparr,
);
echo json_encode($info);
?>
