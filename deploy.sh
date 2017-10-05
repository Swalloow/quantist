#!/bin/bash

ssh ${HOST} -i ~/.ssh/id_rogers -o StrictHostKeyChecking=no << 'ENDSSH'
./setup.sh
exit
ENDSSH