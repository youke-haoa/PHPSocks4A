<?php

$s = socket_create(AF_INET,SOCK_STREAM,SOL_TCP);
if(!$s){
  echo socket_strerror(socket_last_error()). "\n";
  die('socket_create fail.');
}else{echo "socket_create\n";}

$bp = socket_bind($s,'127.0.0.1',3601);
if(!$bp){
  echo socket_strerror(socket_last_error()). "\n";
  die('socket_bind fail.');
}else{echo "socket_bind\n";}

$bl = socket_listen($s);
if(!$bl){
  echo socket_strerror(socket_last_error()). "\n";
  die('socket_listen fail.');
}else{echo "socket_listen\n";}
socket_close($s);


?>