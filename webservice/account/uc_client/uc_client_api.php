<?php
$_SERVER['HTTP_USER_AGENT'] = 'python-uc_client/0.1';
$PROJECT_ROOT = '/data0/www/bbs';
include $PROJECT_ROOT . '/config/config_ucenter.php';
include $PROJECT_ROOT . '/uc_client/client.php';

function safeEncoding($string, $outEncoding='UTF-8')
{
    $encoding = "UTF-8";
    for($i=0;$i<strlen($string);$i++)
    {
        if(ord($string{$i})<128)
            continue;

        if((ord($string{$i})&224)==224)
        {
            //第一个字节判断通过
            $char = $string{++$i};
            if((ord($char)&128)==128)
            {
                //第二个字节判断通过
                $char = $string{++$i};
                if((ord($char)&128)==128)
                {
                    $encoding = "UTF-8";
                    break;
                }
            }
        }
        if((ord($string{$i})&192)==192)
        {
            //第一个字节判断通过
            $char = $string{++$i};
            if((ord($char)&128)==128)
            {
                //第二个字节判断通过
                $encoding = "GB2312";
                break;
            }
        }
    }

    if(strtoupper($encoding) == strtoupper($outEncoding))
        return $string;
    else
        return iconv($encoding,$outEncoding,$string);
}

$func = $argv[1];
if(!is_callable($func))
{
  // command not found
  exit(127);
}

$line = trim(fgets(STDIN));
$func_argv = json_decode($line);
foreach($func_argv as $key => $val)
{
    if(is_string($val))
    {
        $func_argv[$key] = safeEncoding($val, 'gbk');
    }
}

if(!is_array($func_argv))
{
  echo json_encode(null);
  exit(1);
}

$result = call_user_func_array($func, $func_argv);
if(is_array($result))
{
    foreach($result as $key => $val)
    {
        $result[$key] = safeEncoding($val,'UTF-8');
    }
}
echo json_encode($result);
exit(0);
