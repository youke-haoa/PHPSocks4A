<?php
$act=$_GET["act"];
$show=$_GET["show"];
if('start'==$act){
        $show = $act;
        exec('python ~/forward.py 1>>~/forwardlog.txt 2>&1 &');
}

if('stop'==$act){
        $show = $act;
        exec('pkill python');
}

if('restart'==$act){
        $show = $act;
        exec('pkill python && python ~/forward.py 1>>~/forwardlog.txt 2>&1 &');
}

if('clear'==$act){
        $show = $act;
        exec('echo >~/forwardlog.txt');
}
if('' != $show)
{
        echo "</p>";
        echo "<font size='12' color='red'>act='".$act."'</font>";
        echo "</p>";
        echo "<font size='16'><a href='/forwardlog.txt' target='_blank'>forwardlog.txt</a></font>";
        echo "</p>";
        echo "<font size='16'><a href='/forward.php?act=clear'>clear</a></font>";
        echo "</p>";
        echo "<font size='16'><a href='/forward.php?act=start'>start</a></font>";
        echo "</p>";
        echo "<font size='16'><a href='/forward.php?act=stop'>stop</a></font>";
        echo "</p>";
        echo "<font size='16'><a href='/forward.php?act=restart'>restart</a></font>";     
}

?>