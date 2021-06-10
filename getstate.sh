#!/bin/bash
# replace IP address with IP of outlet controller
curl -s -m 5 --header "Content-Type: text/xml;charset=UTF-8" --header 'SOAPAction: "urn:Belkin:service:basicevent:1#GetBinaryState"' -X POST --data @/home/pi/temperature-control/getstatus.xml http://192.168.1.173:49153/upnp/control/basicevent1 | grep '<BinaryState>' | perl -pe 's|<BinaryState>(\d)</BinaryState>|$1|' > powerstate.txt
if [[ $? == "0" ]]; then
  exit 0
fi

curl -s -m 5 --header "Content-Type: text/xml;charset=UTF-8" --header 'SOAPAction: "urn:Belkin:service:basicevent:1#GetBinaryState"' -X POST --data @/home/pi/temperature-control/getstatus.xml http://192.168.1.173:49152/upnp/control/basicevent1 | grep '<BinaryState>' | perl -pe 's|<BinaryState>(\d)</BinaryState>|$1|' > powerstate.txt

if [[ $? == "0" ]]; then
  exit 0
fi
