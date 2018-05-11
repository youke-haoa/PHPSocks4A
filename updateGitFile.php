<?php
exec('export GIT_COMMITTER_NAME=pod && export GIT_COMMITTER_EMAIL=unknow && cd ~/gitFile/ && git pull',$results,$ret);
var_dump($results);
echo '<br/>';
var_dump($ret);
?>