<!DOCTYPE html>
<html>
  <head>
    <title>socket_send</title>
  </head>
  <body>
    <?php 
      $socket = socket_create(AF_INET, SOCK_STREAM, SOL_TCP);
      socket_set_block ( resource $socket );
      $ipaddr = gethostbynamel ( string $hostname )[0];
      socket_connect($socket,ipaddr,80);
      $baiduGet = "Host: www.baidu.com\r\nUser-Agent: Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:58.0) Gecko/20100101 Firefox/58.0\r\nAccept: text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8\r\nAccept-Language: zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2\r\nConnection: keep-alive";
      $baiduBytes = iconv('utf-8','ascii',$baiduGet);
      socket_write( $socket , $baiduBytes);
      $socketStr = serialize($socket);
      $read = socket_read( $socket, 1024 );
      socket_close($sock);
      echo $read;
    ?>
  </body>
</html>