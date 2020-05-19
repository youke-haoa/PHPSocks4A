<?php

$url = $_GET["url"];//目标url
$useBase64=$_GET["base64"];//base64转换
$ref = $_GET["ref"];//设置REFERER

if(null == $url){
	die("null url");
}
if('1'==$useBase64){
	$url = base64_decode($url);
}
if(strpos(strtolower(parse_url($url,PHP_URL_HOST)),"openshift") !== false){//不能访问可能包含自身的网页
	die("openshift is not safe");
}

$ch = curl_init();

curl_setopt($ch, CURLOPT_URL, $url);
curl_setopt($ch, CURLOPT_AUTOREFERER, true);
curl_setopt($ch, CURLOPT_MAXREDIRS, 3);//最多重定向次数

if(null != $ref){
	curl_setopt($ch, CURLOPT_REFERER, $ref);
}
elseif(strpos(strtolower($url),'s1.xiahi.com') !== false){//特殊处理
	curl_setopt($ch, CURLOPT_REFERER, "http://www.tadedy.net/js/player/mp4.html");
}

$reqHeaders = apache_request_headers();//处理请求头中的内容
foreach($reqHeaders as $reqHKey=>$reqHValue){
	if(strtolower($reqHKey)==='range')	{//请求头中包含range则请求时也带上
		$hasRange = true;
		curl_setopt($ch, CURLOPT_RANGE, explode('=',$reqHValue)[1]);
	}
}
//curl_setopt($ch, CURLOPT_HTTPHEADER, $reqRange);

curl_setopt($ch, CURLINFO_HEADER_OUT, true);//可查看请求头
curl_setopt($ch, CURLOPT_HEADER, true);//返回头信息
curl_setopt($ch, CURLOPT_NOBODY, true);//不需要内容部分，HEAD请求
curl_setopt($ch, CURLOPT_RETURNTRANSFER , true);
$headRsp = curl_exec($ch);

if(curl_errno($ch)){   // should be 0
    curl_close($ch);
	die("get header fail");
}

$rspHeadLen = curl_getinfo($ch,CURLINFO_HEADER_SIZE );
$rspHeader = substr($headRsp, 0, $rspHeadLen);//响应头内容

$rspHeadArr = explode("\r\n", $rspHeader);
foreach ($rspHeadArr as $loop) {
	if(strpos(strtolower($loop),"content-range:") !== false){
		header($loop);
	}
	if(strpos(strtolower($loop),"accept-ranges:") !== false){//处理断点续传
		header($loop);
	}
	if(strpos(strtolower($loop),"content-disposition:") !== false){//设置下载文件名
		$hasDisposition = true;
		header($loop);
	}
}

if(null == $hasDisposition){//如果目标没有在头设置文件名，自行设置文件名，但不设置附件
	$urlFileName = pathinfo(parse_url($url,PHP_URL_PATH),PATHINFO_BASENAME);
	if(null != $urlFileName){
		header('Content-Disposition: filename='.$urlFileName);
	}
}

$rspHeaders = curl_getinfo($ch);
if(null != $rspHeaders){//设置响应(断点续传)
	header('Content-type: '.$rspHeaders['content_type'],true,$rspHeaders['http_code']);
	header('Content-Length: '.$rspHeaders['download_content_length']);
}
//$rspCode = curl_getinfo($ch, CURLINFO_HTTP_CODE);

$reqMethod = $_SERVER['REQUEST_METHOD'];
if('HEAD' == $reqMethod){//支持HEAD请求
	curl_close($ch);
	header("MTDHEAD: true");
	return;
}

curl_setopt($ch, CURLOPT_HEADER, false);
curl_setopt($ch, CURLOPT_NOBODY, false);
curl_setopt($ch, CURLOPT_RETURNTRANSFER , false);

curl_exec($ch);
curl_close($ch);
?>