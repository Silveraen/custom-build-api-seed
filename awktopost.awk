#!/usr/local/bin/gawk -f
BEGIN {
	
}

{
    cmd = "curl";
    cmd;
    close(cmd, "to");
    cmd " -d '" $0 "' -H 'content-type:application/json' 'http://localhost:5000/yaybirds/'" |& getline result;
    print result;
}

END {
	
}
