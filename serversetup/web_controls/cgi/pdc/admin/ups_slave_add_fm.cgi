#!/bin/bash
#Copyright (C) 2010  Paul Sharrad

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

#Language
############################
#Language
############################

STYLESHEET=defaultstyle.css
TIMEOUT=300
NOTIMEOUT=127.0.0.1
MOBILE=no
[ -f /opt/karoshi/web_controls/user_prefs/$REMOTE_USER ] && source /opt/karoshi/web_controls/user_prefs/$REMOTE_USER
TEXTDOMAIN=karoshi-server

#Check if timout should be disabled
if [ `echo $REMOTE_ADDR | grep -c $NOTIMEOUT` = 1 ]
then
	TIMEOUT=86400
fi

#########################
#Get data input
#########################
TCPIP_ADDR=$REMOTE_ADDR
DATA=`cat | tr -cd 'A-Za-z0-9\._:%\-'`

END_POINT=9
#Assign UPSSERVER
COUNTER=2
while [ $COUNTER -le $END_POINT ]
do
	DATAHEADER=`echo $DATA | cut -s -d'_' -f$COUNTER`
	if [ `echo $DATAHEADER'check'` = UPSSERVERcheck ]
	then
		let COUNTER=$COUNTER+1
		UPSSERVERDATA=$(echo $DATA | cut -s -d'_' -f$COUNTER | sed 's/%2C/,/g')
		UPSSERVER=$(echo "$UPSSERVERDATA" | cut -d, -f1)
		UPSMODEL=$(echo "$UPSSERVERDATA" | cut -d, -f2)
		break
	fi
	let COUNTER=$COUNTER+1
done

#Get current date and time
DAY=`date +%d`
MONTH=`date +%m`
YEAR=`date +%Y`

HOUR=`date +%H`
MINUTES=`date +%M`
SECONDS=`date +%S`

function show_status {
echo '<SCRIPT language="Javascript">'
echo 'alert("'$MESSAGE'")';
echo 'window.location = "/cgi-bin/admin/ups_add_fm.cgi";'
echo '</script>'
echo "</div></body></html>"
exit
}

echo "Content-type: text/html"
echo ""
echo '<!DOCTYPE html><html><head><meta http-equiv="Content-Type" content="text/html; charset=utf-8"><title>'$"Add a slave UPS"'</title><meta http-equiv="REFRESH" content="'$TIMEOUT'; URL=/cgi-bin/admin/logout.cgi"><link rel="stylesheet" href="/css/'$STYLESHEET'?d='$VERSION'"><script language="JavaScript" src="/all/calendar/ts_picker.js" type="text/javascript"></script>
        <!-- Timestamp input popup (European Format) --><script src="/all/stuHover.js" type="text/javascript"></script>
<script src="/all/js/jquery.js"></script>
<script src="/all/js/jquery.tablesorter/jquery.tablesorter.js"></script>
<script id="js">
$(document).ready(function() 
    { 
        $("#myTable").tablesorter(); 
    } 
);
</script>
</head>
<body onLoad="start()"><div id="pagecontainer">'
#########################
#Check https access
#########################
if [ https_$HTTPS != https_on ]
then
	export MESSAGE=$"You must access this page via https."
	show_status
fi
#########################
#Check user accessing this script
#########################
if [ ! -f /opt/karoshi/web_controls/web_access_admin ] || [ $REMOTE_USER'null' = null ]
then
	MESSAGE=$"You must be a Karoshi Management User to complete this action."
	show_status
fi

if [ `grep -c ^$REMOTE_USER: /opt/karoshi/web_controls/web_access_admin` != 1 ]
then
	MESSAGE=$"You must be a Karoshi Management User to complete this action."
	show_status
fi
#Generate navigation bar
/opt/karoshi/web_controls/generate_navbar_admin
echo '<form action="/cgi-bin/admin/ups_slave_add.cgi" name="tstest" method="post"><div id="actionbox3"><div id="titlebox"><table class="standard" style="text-align: left;" ><tbody><tr>
<td><div class="sectiontitle">'$"Add a slave UPS"'</div></td>
<td style="vertical-align: top;">
<button class="button" formaction="ups_status.cgi" name="_UPSStatus" value="_">
'$"UPS Status"'
</button>
</td>
<td><a class="info" href="javascript:void(0)"><img class="images" alt="" src="/images/help/info.png"><span>'$"This will configure a UPS device connected to a server."'</span></a></td></tr></tbody></table><br></div><div id="infobox">'


#Check to see if there are any master ups available

if [ ! -d /opt/karoshi/server_network/ups/master ]
then
	MESSAGE=$"There are no master UPS devices available."
	show_status
fi

if [ `ls -1 /opt/karoshi/server_network/ups/master/ | wc -l` = 0 ]
then
	MESSAGE=$"There are no master UPS devices available."
	show_status
fi

echo '<table class="standard" style="text-align: left;" ><tbody>
<tr><td style="width: 180px;">'$"Master UPS"'</td>
        <td>'
if [ -z "$UPSSERVER" ]
then
	#Generate list of UPC data
	echo '<select name="_UPSSERVER_" style="width: 200px;"><option> </option>'

	for UPSSERVERS in /opt/karoshi/server_network/ups/master/*
	do
		UPSSERVER=`basename $UPSSERVERS`
		if [ -d /opt/karoshi/server_network/ups/master/$UPSSERVER/drivers/ ]
		then
			if [ `ls -1 /opt/karoshi/server_network/ups/master/$UPSSERVER/drivers/ | wc -l` != 0 ]
			then
				for UPSMODELS in /opt/karoshi/server_network/ups/master/$UPSSERVER/drivers/*
				do
					UPSMODEL=`basename $UPSMODELS`
					echo '<option value="'$UPSSERVER','$UPSMODEL'">'$UPSSERVER': '$UPSMODEL'</option>'
				done
			fi
		fi
	done
	echo '</select>'
else
	echo '<input type="hidden" name="_UPSSERVER_" value="'$UPSSERVER','$UPSMODEL'">'$UPSSERVER' : '$UPSMODEL''
fi


echo '</td>'

[ -z "$UPSSERVER" ] && echo '<td><a class="info" href="javascript:void(0)"><img class="images" alt="" src="/images/help/info.png"><span>'$"Choose a master UPS device from the list."'</span></a></td>'

echo '</tr></tbody></table><br><br>'

#Show list of ssh enabled servers that do not have a main UPS
/opt/karoshi/web_controls/show_servers $MOBILE addslaveups $"Add slave ups"
echo '</div></div></form></div></body></html>'
exit

