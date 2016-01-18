#!/bin/bash
#Copyright (C) 2012  Paul Sharrad

#This file is part of Karoshi Server.
#
#Karoshi Server is free software: you can redistribute it and/or modify
#it under the terms of the GNU Affero General Public License as published by
#the Free Software Foundation, either version 3 of the License, or
#(at your option) any later version.
#
#Karoshi Server is distributed in the hope that it will be useful,
#but WITHOUT ANY WARRANTY; without even the implied warranty of
#MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#GNU Affero General Public License for more details.
#
#You should have received a copy of the GNU Affero General Public License
#along with Karoshi Server.  If not, see <http://www.gnu.org/licenses/>.

#
#The Karoshi Team can be contacted at: 
#mpsharrad@karoshi.org.uk
#jsharrad@karoshi.org.uk

#
#Website: http://www.karoshi.org.uk

##########################
#Language
##########################

STYLESHEET=defaultstyle.css
[ -f /opt/karoshi/web_controls/user_prefs/$REMOTE_USER ] && source /opt/karoshi/web_controls/user_prefs/$REMOTE_USER
TEXTDOMAIN=karoshi-server

##########################
#Show page
##########################
echo "Content-type: text/html"
echo ""
echo '<!DOCTYPE html>
<html>
<head>
<meta http-equiv="Content-Type" content="text/html; charset=utf-8"
<link rel="stylesheet" href="/css/'$STYLESHEET'?d='`date +%F`'"><meta http-equiv="REFRESH" content="0;url=helpdesk_set_defaults_fm.cgi"><title>'$"Help Desk"'</title></head><body><div id="pagecontainer">'
#########################
#Get data input
#########################
TCPIP_ADDR=$REMOTE_ADDR
DATA=`cat | tr -cd 'A-Za-z0-9\.%+_:\-'`
#########################
#Assign data to variables
#########################
END_POINT=9
#Assign DEFAULTNAME
COUNTER=2
while [ $COUNTER -le $END_POINT ]
do
DATAHEADER=`echo $DATA | cut -s -d'_' -f$COUNTER`
if [ `echo $DATAHEADER'check'` = DEFAULTNAMEcheck ]
then
let COUNTER=$COUNTER+1
DEFAULTNAME=`echo $DATA | cut -s -d'_' -f$COUNTER`
break
fi
let COUNTER=$COUNTER+1
done
#Assign DEFAULTPRIORITY
COUNTER=2
while [ $COUNTER -le $END_POINT ]
do
DATAHEADER=`echo $DATA | cut -s -d'_' -f$COUNTER`
if [ `echo $DATAHEADER'check'` = DEFAULTPRIORITYcheck ]
then
let COUNTER=$COUNTER+1
DEFAULTPRIORITY=`echo $DATA | cut -s -d'_' -f$COUNTER`
break
fi
let COUNTER=$COUNTER+1
done

function show_status {
echo '<SCRIPT language="Javascript">'
echo 'alert("'$MESSAGE'")';
echo 'window.location = "/cgi-bin/admin/helpdesk_set_defaults_fm.cgi";'
echo '</script>'
echo "</div></body></html>"
exit
}
#########################
#Check https access
#########################
if [ https_$HTTPS != https_on ]
then
export MESSAGE=$"You must access this page via https."
show_status
fi

#########################
#Check data
#########################

#Check to see that NAME is not blank
if [ $DEFAULTNAME'null' = null ]
then
MESSAGE=$"You have not entered in your name."
show_status
fi

#Check to see that DEFAULTPRIORITY is not blank
if [ $DEFAULTPRIORITY'null' = null ]
then
MESSAGE=$"You have not chosen a category."
show_status
fi

#Add in defaults
if [ $DEFAULTNAME = NODEFAULTNAME ]
then
[ /opt/karoshi/server_network/helpdesk/defaultassign ] && rm -f /opt/karoshi/server_network/helpdesk/defaultassign
else
echo $DEFAULTNAME > /opt/karoshi/server_network/helpdesk/defaultassign
fi

if [ $DEFAULTPRIORITY = NODEFAULTPRIORITY ]
then
[ /opt/karoshi/server_network/helpdesk/defaultpriority ] && rm -f /opt/karoshi/server_network/helpdesk/defaultpriority
else
echo $DEFAULTPRIORITY > /opt/karoshi/server_network/helpdesk/defaultpriority
fi

exit

