<?php
$t1=microtime(true);
$t0=$_GET["t0"];
$info=array(
        "t0"=>$t0,
        "t1"=>$t1,
        "t2"=>microtime(true),
);

echo json_encode($info);
?>