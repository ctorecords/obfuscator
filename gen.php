<?php

$opts = getopt('f:');

$files = isset($opts['f']) ? $opts['f'] : [];
if(!is_array($files)) {
    $files = [$files];
}

function getLines($files) {
    if(empty($files)) {
        while ($row = fgets(STDIN)) {
            yield trim($row);
        }
    } else {
        foreach ($files as $file) {
            $f = fopen($file, 'r');
            while ($row = fgets($f)) {
                yield trim($row);
            }
        }
    }
}

function random_value_cb($r) {
    return function () use ($r) { return $r[mt_rand(0, count($r) - 1)]; };
}

$regex = [
    '/[A-ZА-ЯЁ]/u' => random_value_cb(range('A','Z')),
    '/[a-zа-яё]/u' => random_value_cb(range('a','z')),
    '/\d/'         => random_value_cb(range(0, 9)),
];
$results = [];

foreach (getLines($files) as $row) {
    $cols = explode("\t", $row);
    foreach ($cols as &$input) {
        $key = $input;
        if (!array_key_exists($input, $results)) {
            $input = preg_replace_callback_array($regex, $input);
            $results[$key] = $input;
        } else {
            $input = $results[$key];
        }
    }
    echo implode("\t", $cols).PHP_EOL;
}
