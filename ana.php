<html>
<head>
	<meta name="viewport" content="width=device-width, initial-scale=1.0,maximum-scale=1.0, user-scalable=no"/>
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
$domain = "http://s4-ps.apps.us-west-1.starter.openshift-online.com/pp.php?base64=1&url=";
$url = $_POST["targetURL"];//目标url

$urlArr = parse_url($url);
$urlHost = $urlArr['host'];

function URLReq($str) {
	$ch = curl_init();

	curl_setopt($ch, CURLOPT_URL, $url);
	curl_setopt($ch, CURLOPT_AUTOREFERER, true);
	curl_setopt($ch, CURLOPT_MAXREDIRS, 3);//最多重定向次数

	curl_setopt($ch, CURLOPT_RETURNTRANSFER , true);
	return curl_exec($ch);
}

$rsp =URLReq($url);

//取出所有剧集
$vlink_1 = 'id="vlink_1"';
$start2end = strstr($rsp,$vlink_1);
if(! $str2end){
	die("not find vlink_1");
}
$videoUl = strstr($start2end,'</ul>',true);

$urlArry = array();
while(true){
	$hrefStart = strstr($videoUlStr,"href='");
	if(!$hrefStart){//没有找到剧集就返回
		break;
	}
	$nexturl = strstr($hrefStart,"' target=",true);
	$nexturl = str_replace("href='", "", $nexturl);
	$nexturl = $urlHost.$nexturl;
	array_push($urlArry,$nexturl);
	$hrefStart = strstr($hrefStart,"' target=");
}
if(0 == count($urlArry)){//没有剧集就返回
	die("not find href");
}

$videoBase64Url = array();
foreach ($urlArry as $urlValue) {
	$videoRsp = URLReq($urlValue);
	$videoKey = 'now=base64decode("';
	$videoStart = strstr($videoRsp,$videoKey);
	$videoBase64 = strstr($videoStart,'");',true);
	$videoBase64 = str_replace($videoKey, "", $videoBase64);
	array_push($videoBase64Url,$videoBase64);
}

$unescapeStr = strstr($str2end,'")',true);
$unescapeStr = str_replace('VideoInfoList=unescape("', "", $unescapeStr);

function escape($str) {
  return str_replace('\\u', '%u', substr(json_encode($str), 1, -1));
}
function unescape($str) {
  return urldecode(json_decode('"'.str_replace('%u', '\\u', $str).'"'));
}

$videoUrls = array();
foreach($videoBase64Url as $loop){//显示下载链接
	$videoUrl = base64_decode($loop);
	array_push($videoUrls,$videoUrl);
	echo '<br/>';
	echo '<a target="_blank" href="'.$domain.$loop.'">'.$videoUrl.'</a>';
	echo '<br/>';
}
echo '<span>URL Text:</span><br/>';

foreach($videoUrls as $loop){//显示下载链接
	echo '<br/>';
	echo '<span>'.$loop.'</span>';
	echo '<br/>';
}

echo '<br/>';

?>

</body>
</html>
