<?php 

$token='wx123';
$method=$_SERVER['REQUEST_METHOD'];
if('GET'==$method){
  $signature=$_GET["signature"];
  $timestamp=$_GET["timestamp"];
  $nonce=$_GET["nonce"];
  $echostr=$_GET["echostr"];
  $tmpArr = array($token,$timestamp, $nonce);
  sort($tmpArr, SORT_STRING);
  $tmpStr = implode( $tmpArr );
  $tmpStr = sha1( $tmpStr );
  if($tmpStr==$signature){
    echo $echostr;
  }else{
    echo 'fail';
  }
}
if('POST'==$method){
  $inputPost = file_get_contents("php://input");
  $inputXml = simplexml_load_string($inputPost);
  $xmlDoc = new DOMDocument('1.0','utf-8');
  $xmlDoc->formatOutput = true;
  $xmlTag = $xmlDoc->createElement('xml');
  $ToUserNameTag = $xmlDoc->createElement('ToUserName');
  $FromUserNameTag=$xmlDoc->createElement('FromUserName');
  $CreateTimeTag=$xmlDoc->createElement('CreateTime');
  $MsgTypeTag=$xmlDoc->createElement('MsgType');
  $ContentTag=$xmlDoc->createElement('Content');
  $ToText = $xmlDoc->createTextNode($inputXml->FromUserName);
  $FrText = $xmlDoc->createTextNode($inputXml->ToUserName);
  $CrText = $xmlDoc->createtTextNode(intval(time()));
  $MsText= $xmlDoc->createTextNode('text');
  $CoText=$xmlDoc->createTextNode('test');
  $ToUserNameTag->appendChild($ToText);
  $FromUserNameTag->appendChild($FrText);
  $CreateTimeTag->appendChild($CrText);
  $MsgTypeTag->appendChild($MsText);
  $ContentTag->appendChild($CoText);
  $xmlTag->appendChild($ToUserNameTag);
  $xmlTag->appendChild($FromUserNameTag);
  $xmlTag->appendChild($CreateTimeTag);
  $xmlTag->appendChild($MsgTypeTag);
  $xmlTag->appendChild($ContentTag);
  $xmlDoc->appendChild($xmlTag);

  echo $xml->asXML();
  
}
?>
