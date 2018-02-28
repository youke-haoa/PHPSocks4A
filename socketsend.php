<!DOCTYPE html>
<html>
  <head>
    <title>socket_send</title>
  </head>
  <body>
    <?php 
      $socket = socket_create(AF_INET, SOCK_STREAM, SOL_TCP);
      socket_set_block ($socket );
      $ipaddr = gethostbynamel ('ip.cn')[0];
      echo $ipaddr;
      echo '<br/>';
      $conR = socket_connect($socket,$ipaddr,80);
      echo $conR ;
      echo '<br/>';
      $baiduGet = "GET / HTTP/1.1\r\nHost: ip.cn\r\nUser-Agent: Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:58.0) Gecko/20100101 Firefox/58.0\r\nAccept: text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8\r\nAccept-Language: zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2\r\nConnection: keep-alive\r\n\r\n";
      $baiduBytes = iconv('utf-8','ascii',$baiduGet);
      $writeC = socket_write( $socket , $baiduBytes);
      echo $writeC;
      echo '<br/>===recv====<br/>';
      //$socketStr = serialize($socket);
      $read = socket_read( $socket, 10240 );
      echo $read;
      socket_close($socket);
    ?>
  </body>
</html>