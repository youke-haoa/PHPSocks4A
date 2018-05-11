<?php

exec('ls /',$results,$ret);

echo  $results[0] . "<br/>";
echo  $results[1]. "<br/>";
echo  $results[2]. "<br/>";
echo  $ret;
?>