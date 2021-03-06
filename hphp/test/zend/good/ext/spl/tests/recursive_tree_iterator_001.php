<?hh
<<__EntryPoint>> function main(): void {
$ary = darray[
	0 => varray[
		"a",
		1,
	],
	"a" => darray[
		0 => 2,
		1 => "b",
		3 => varray[
			4,
			"c",
		],
		"3" => varray[
			4,
			"c",
		],
	],
];

$it = new RecursiveArrayIterator($ary);
echo "-- flags = BYPASS_KEY --\n";
foreach(new RecursiveTreeIterator($it) as $k => $v) {
	$v = HH\is_any_array($v) ? 'Array' : $v; echo "[$k] => $v\n";
}
echo "-- flags = BYPASS_CURRENT --\n";
foreach(new RecursiveTreeIterator($it, RecursiveTreeIterator::BYPASS_CURRENT) as $k => $v) {
	$v = HH\is_any_array($v) ? 'Array' : $v; echo "[$k] => $v\n";
}
echo "-- flags = BYPASS_KEY|BYPASS_KEY --\n";
foreach(new RecursiveTreeIterator($it, RecursiveTreeIterator::BYPASS_CURRENT|RecursiveTreeIterator::BYPASS_KEY) as $k => $v) {
	$v = HH\is_any_array($v) ? 'Array' : $v; echo "[$k] => $v\n";
}
echo "-- flags = 0 --\n";
foreach(new RecursiveTreeIterator($it, 0) as $k => $v) {
	$v = HH\is_any_array($v) ? 'Array' : $v; echo "[$k] => $v\n";
}
echo "-- flags = 0, caching_it_flags = CachingIterator::CATCH_GET_CHILD --\n";
foreach(new RecursiveTreeIterator($it, 0, CachingIterator::CATCH_GET_CHILD) as $k => $v) {
	$v = HH\is_any_array($v) ? 'Array' : $v; echo "[$k] => $v\n";
}

echo "===DONE===\n";
}
