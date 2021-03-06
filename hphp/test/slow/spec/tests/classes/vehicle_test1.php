<?hh
<<__EntryPoint>>
function main_entry(): void {
  error_reporting(-1);

  include_once 'Vehicle.inc';
  include_once 'Aircraft.inc';
  include_once 'PassengerJet.inc';

  // $v = new Vehicle;        // can't instantiate an abstract class
  // $a = new Aircraft;       // can't instantiate an abstract class

  $pj = new PassengerJet("Horizon", 1993, 33000, 235);
  echo "\$pj's maximum speed: " . $pj->getMaxSpeed() . "\n";
  echo "\$pj's maximum altitude: " . $pj->getMaxAltitude() . "\n";
}
