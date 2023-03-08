 #!/bin/bash
 sudo twingate start
 /usr/bin/twingate-notifier console
 #twingate resources --all
 twingate auth "home cidr update"
 twingate resources --all