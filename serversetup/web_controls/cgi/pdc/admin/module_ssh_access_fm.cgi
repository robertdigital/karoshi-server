#!/bin/bash
#Copyright (C) 2007  Paul Sharrad

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
############################
#Language
############################

STYLESHEET=defaultstyle.css
TIMEOUT=300
NOTIMEOUT=127.0.0.1
[ -f /opt/karoshi/web_controls/user_prefs/$REMOTE_USER ] && source /opt/karoshi/web_controls/user_prefs/$REMOTE_USER
TEXTDOMAIN=karoshi-server


#Check if timout should be disabled
if [ `echo $REMOTE_ADDR | grep -c $NOTIMEOUT` = 1 ]
then
TIMEOUT=86400
fi
############################
#Show page
############################
echo "Content-type: text/html"
echo ""
echo '
<!DOCTYPE html><html><head><meta http-equiv="Content-Type" content="text/html; charset=utf-8">
  <title>'$"Remote SSH Access"'</title><meta http-equiv="REFRESH" content="'$TIMEOUT'; URL=/cgi-bin/admin/logout.cgi">
<link rel="stylesheet" href="/css/'$STYLESHEET'?d='`date +%F`'">
<script src="/all/stuHover.js" type="text/javascript"></script>
</head>
<body onLoad="start()"><div id="pagecontainer">'

#########################
#Get data input
#########################
TCPIP_ADDR=$REMOTE_ADDR
#DATA=`cat | tr -cd 'A-Za-z0-9\._:\-'`
DATA=`cat | tr -cd 'A-Za-z0-9\._:%\-+'`
#########################
#Assign data to variables
#########################
END_POINT=5
#Assign SERVERNAME

COUNTER=2
while [ $COUNTER -le $END_POINT ]
do
DATAHEADER=`echo $DATA | cut -s -d'_' -f$COUNTER`
if [ `echo $DATAHEADER'check'` = SERVERNAMEcheck ]
then
let COUNTER=$COUNTER+1
SERVERNAME=`echo $DATA | cut -s -d'_' -f$COUNTER`
break
fi
let COUNTER=$COUNTER+1
done

function show_status {
echo '<SCRIPT language="Javascript">'
echo 'alert("'$MESSAGE'")';
echo 'window.location = "/cgi-bin/admin/karoshi_servers_view.cgi"'
echo '</script>'
echo "</div></body></html>"
exit
}

#Generate navigation bar
/opt/karoshi/web_controls/generate_navbar_admin

#########################
#Check data
#########################
#Check to see that servername is not blank
if [ $SERVERNAME'null' = null ]
then
MESSAGE=$"The server cannot be blank."
show_status
fi

echo '<form action="/cgi-bin/admin/module_ssh_access.cgi" method="post"><div id="actionbox"><div class="sectiontitle">'$"Remote SSH Access"' - '$SERVERNAME'</div><br>
<input name="_SERVERNAME_" value="'$SERVERNAME'" type="hidden">
<b>'$"Description"'</b><br><br>
'$"This module is for advanced use for users that want ssh access to the main server."' '$"It can also be used to join this server to another Karoshi system via the federated server module so that when users are created on the master system they will also be created here."'<br><br>
<b>'$"Parameters"'</b><br><br>
<table class="standard" style="text-align: left;" border="0" cellpadding="2" cellspacing="0"><tbody>
<tr><td style="width: 180px;">'$"TCPIP"' / '$"MAC"'</td><td><input tabindex= "2" name="_TCPIP_" size="20" type="text"></td><td>
<select name="_RESTRICTTYPE_">
<option>TCPIP</option>
<option>MAC</option>
</select>
</td><td><a class="info" href="javascript:void(0)"><img class="images" alt="" src="/images/help/info.png"><span>'$"Enter in TCPIP numbers or MAC addresses (separated by commas) for machines you want to restrict access to. Leave this blank for unrestricted access."'</span></a></td></tr>
</tbody></table><br><br>
</div>
<div id="submitbox">
<input value="'$"Submit"'" class="button" type="submit"> <input value="'$"Reset"'" class="button" type="reset">
</div>
</form>
</div></body>
</html>
'
exit
