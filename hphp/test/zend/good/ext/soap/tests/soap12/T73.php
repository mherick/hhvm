<?hh
<<__EntryPoint>>
function entrypoint_T73(): void {
  $GLOBALS['HTTP_RAW_POST_DATA'] = <<<EOF
<?xml version='1.0' ?>
<env:Envelope xmlns:env="http://www.w3.org/2003/05/soap-envelope"
              xmlns:xsd="http://www.w3.org/2001/XMLSchema"
              xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">
  <env:Body>
    <test:echoString xmlns:test="http://example.org/ts-tests"
                      env:encodingStyle="http://www.w3.org/2003/05/soap-encoding">
      <test:inputString xsi:type="xsd:string"
            env:encodingStyle="http://www.w3.org/2003/05/soap-encoding">hello world</test:inputString>
    </test:echoString>
  </env:Body>
</env:Envelope>
EOF;
  include "soap12-test.inc";
  test();
}
