<html>
<head>
    <meta http-equiv="Content-Type" content="text/html; charset=utf-8" />
    <meta http-equiv="Content-Language" content="zh-CN" />
    <title>分析</title>
</head>
<body>
<!--  -->
<form action="#" method="POST">
</br>
<span>目标URL:</span><input type="text" name="targetURL"/>
<br/>
<br/>
<input type="reset"/>
<span>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</span>
<span>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</span>
<input type="submit"/>
</form>
<!--  -->
<span>URL:</span><br/>
<?php

if('POST' !== $_SERVER['REQUEST_METHOD']){
	die();
}
$domain = "http://s4-ps.apps.us-west-1.starter.openshift-online.com/pp.php?url=";
$url = $_POST["targetURL"];//目标url

$ch = curl_init();

curl_setopt($ch, CURLOPT_URL, $url);
curl_setopt($ch, CURLOPT_AUTOREFERER, true);
curl_setopt($ch, CURLOPT_MAXREDIRS, 3);//最多重定向次数

curl_setopt($ch, CURLOPT_RETURNTRANSFER , true);
$rsp = curl_exec($ch);

//取出下载列表
$str2end = strstr($rsp,'VideoInfoList=unescape("');
if(! $str2end){
	die("not find VideoInfoList");
}
$unescapeStr = strstr($str2end,'")',true);
$unescapeStr = str_replace('VideoInfoList=unescape("', "", $unescapeStr);

function escape($str) {
  return str_replace('\\u', '%u', substr(json_encode($str), 1, -1));
}
function unescape($str) {
  return urldecode(json_decode('"'.str_replace('%u', '\\u', $str).'"'));
}
//下载列表转义
$vList = unescape($unescapeStr);

$vListArr = explode("$", $vList);
$pathArr = array();

foreach($vListArr as $loop){//挑选下载文件地址
	if(strpos(strtolower($loop),"http") !== false){//设置下载文件名
		$pathArr[]=$loop;
	}
}
foreach($pathArr as $loop){//显示下载链接
	echo '<br/>';
	echo '<a href="'.$domain.$loop.'">'.$loop.'</a>';
	echo '<br/>';
}

?>

</body>
</html>
