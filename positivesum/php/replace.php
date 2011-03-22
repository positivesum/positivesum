<?php
/**

 This script takes a string in STDIN and 2 arguments($from and $to)

= Syntax =

echo 'string' | php replace.php http://from http://to
 
= Testing =

# test string input
php -r "fwrite(STDOUT, serialize('<h2><a href="http://dnh.sr.hstd.org">DNH</a></h2>'));" | php replace.php http://dnh.sr.hstd.org http://dnh

# test serialized array input
php -r "fwrite(STDOUT, serialize(array('<h3><a href="http://dnh.sr.hstd.org">DNH H3</a></h3>', '<h2><a href="http://dnh.sr.hstd.org">DNH</a></h2>')));" | php replace.php http://dnh.sr.hstd.org http://dnh

*/

#error_reporting(E_ALL);

include('html/wp-includes/functions.php');

function recursive_array_replace($find, $replace, &$data) {
    if (is_array($data)) {
        foreach ($data as $key => $value) {
            if (is_array($value)) {
                recursive_array_replace($find, $replace, $data[$key]);
            } else {
                if (is_string($value)) $data[$key] = str_replace($find, $replace, $value);
            }
        }
    } else {
      if (is_string($data)) $data = str_replace($find, $replace, $data);
    }
	return $data;
}

array_shift($argv); //to get the command line arguments, removed the first parameter

$from = $argv[0];
$to = $argv[1];

$lines = file_get_contents("php://stdin");

$output = '';

if ( is_serialized($lines) ) {
	if ( $array = unserialize($lines) ) {
		$replaced = recursive_array_replace($from, $to, $array);
		$output = serialize($replaced);
	}
} else {
   	$output = str_replace($from, $to, $lines);
}

fwrite(STDOUT, $output);

?>
