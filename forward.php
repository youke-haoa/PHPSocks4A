<?php
$act=$_GET["act"];
if('start'==$act){
        exec('python ~/forward.py >>~/forwardlog.txt 2>&1 &');
}

if('stop'==$act){
        exec('pkill python');
}

if('restart'==$act){
        exec('pkill python && python ~/forward.py >>~/forwardlog.txt 2>&1 &');
}

if('clear'==$act){
        exec('echo >~/forwardlog.txt');
}
echo "</p>";
echo "<font size='12' color='red'>act='".$act."'</font>";
echo "</p>";
echo "<font size='16'><a href='/forwardlog.txt'>forwardlog.txt</a></font>";

?>