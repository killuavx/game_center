<?php
$_SERVER['HTTP_USER_AGENT'] = 'python-uc_client/0.1';
$PROJECT_ROOT = '/data0/www/bbs';
include $PROJECT_ROOT . '/config/config_ucenter.php';
include $PROJECT_ROOT . '/uc_client/client.php';

$func = $argv[1];
if(!is_callable($func))
{
  // command not found
  exit(127);
}

$line = trim(fgets(STDIN));
$func_argv = json_decode($line);
if(!is_array($func_argv))
{
  echo json_encode(null);
  exit(1);
}

$result = call_user_func_array($func, $func_argv);
echo json_encode($result);
exit(0);
