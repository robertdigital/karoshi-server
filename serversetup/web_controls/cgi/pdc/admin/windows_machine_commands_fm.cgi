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
############################
#Language
############################

STYLESHEET=defaultstyle.css
TIMEOUT=300
NOTIMEOUT=127.0.0.1
[ -f /opt/karoshi/web_controls/user_prefs/"$REMOTE_USER" ] && source /opt/karoshi/web_controls/user_prefs/"$REMOTE_USER"
export TEXTDOMAIN=karoshi-server

#Check if timout should be disabled
if [[ $(echo "$REMOTE_ADDR" | grep -c "$NOTIMEOUT") = 1 ]]
then
	TIMEOUT=86400
fi
############################
#Show page
############################
echo "Content-type: text/html"
echo ""
echo '
<!DOCTYPE html><html><head><meta http-equiv="Content-Type" content="text/html; charset=utf-8"><title>'$"Windows Commands"'</title><meta http-equiv="REFRESH" content="'"$TIMEOUT"'; URL=/cgi-bin/admin/logout.cgi"><link rel="stylesheet" href="/css/'"$STYLESHEET"'?d='"$VERSION"'"><script src="/all/stuHover.js" type="text/javascript"></script><meta name="viewport" content="width=device-width, initial-scale=1"> <!--480--></head>
<body onLoad="start()"><div id="pagecontainer">'

#Detect mobile browser
MOBILE=no
source /opt/karoshi/web_controls/detect_mobile_browser
source /opt/karoshi/web_controls/version

#Redirect to windows_servers_add_fm.cgi if no windows servers have been added
if [ ! -d /opt/karoshi/server_network/windows_servers/ ]
then
	echo '<form action="windows_servers_add_fm.cgi" method="post">/form>
	<SCRIPT LANGUAGE="JavaScript">document.forms[0].submit();</SCRIPT>'
fi

#Generate navigation bar
if [ "$MOBILE" = no ]
then
	DIV_ID=actionbox
	#Generate navigation bar
	/opt/karoshi/web_controls/generate_navbar_admin
else
	DIV_ID=menubox
fi
echo '<form action="/cgi-bin/admin/windows_machine_commands.cgi" method="post"><div id="'"$DIV_ID"'">'

#Show back button for mobiles
if [ "$MOBILE" = yes ]
then
	echo '<table class="standard" style="text-align: left;">
	<tbody><tr><td style="vertical-align: top;"><a href="/cgi-bin/admin/mobile_menu.cgi"><img border="0" src="/images/submenus/mobile/back.png" alt="'$"Back"'"></a></td>
	<td style="vertical-align: middle;"><a href="/cgi-bin/admin/mobile_menu.cgi"><b>'$"Windows Commands"'</b></a></td><td><a class="info" href="javascript:void(0)"><img class="images" alt="" src="/images/help/info.png"><span>'$"This will send commands to a windows machine joined to your network."'</span></a></td></tr></tbody></table>'
else
	echo '<b>'$"Windows Commands"'</b> <a class="info" href="javascript:void(0)"><img class="images" alt="" src="/images/help/info.png"><span>'$"This will send commands to a windows machine joined to your network."'</span></a><br><br>'
fi

echo '
  <table class="standard" style="text-align: left;" >
    <tbody>
<tr>
         <td style="width: 180px;">'$"Command"'</td>
        <td>
        <select name="_COMMAND_" style="width: 200px;">
        <option></option>
	<option value="shutdown">'$"Shutdown"'</option>
        <option value="restart">'$"Restart"'</option>
	<option value="abortshutdown">'$"Abort shutdown"'</option>
	<option value="startservice">'$"Start service"'</option>
	<option value="stopservice">'$"Stop service"'</option>
	<option value="servicestatus">'$"Service status"'</option>'
#	<option value="showprinters">'$"Show printers"'</option>
echo	'<option value="showshares">'$"Show shares"'</option>
	<option value="showfiles">'$"Show open files"'</option>
	</select></td><td>
<a class="info" href="javascript:void(0)"><img class="images" alt="" src="/images/help/info.png"><span>'$"Choose the command that you want to be carried out."'</span></a>
      </td></tr>
      <tr>
        <td>'$"Extra options"'</td>
        <td><input tabindex= "5" name="_OPTIONS_" style="width: 200px;" size="20" type="text"></td><td>
<a class="info" href="javascript:void(0)"><img class="images" alt="" src="/images/help/info.png"><span>'$"If a command needs extra options you can add them here."'</span></a>
      </td>
      </tr>
    </tbody>
  </table><br>'

#Show list of enabled servers
SERVERLISTARRAY=( `ls -1 /opt/karoshi/server_network/windows_servers/` )
SERVERLISTCOUNT=${#SERVERLISTARRAY[@]}
SERVERCOUNTER=0
SERVERICON="/images/submenus/system/computer.png"
SERVERICON2="/images/submenus/system/all_computers.png"
echo '<table class="standard" style="text-align: left;" ><tbody><tr>'
while [ "$SERVERCOUNTER" -lt "$SERVERLISTCOUNT" ]
do
	KAROSHISERVER="${SERVERLISTARRAY[$SERVERCOUNTER]}"
	echo '<td style="width: 90px; vertical-align: top; text-align: left;">
	<button class="info" name="_Server_" value="_SERVER_'"$KAROSHISERVER"'_">
	<img src="'$SERVERICON'" alt="'"$KAROSHISERVER"'">
	<span>'"$KAROSHISERVER"'</span>
	</button>
	<br>'"$KAROSHISERVER"'</td>'
	[ "$SERVERCOUNTER" = 5 ] && echo '</tr><tr>'
	let SERVERCOUNTER="$SERVERCOUNTER"+1
done
echo '</tr><tr><td style="width: 90px; vertical-align: top; text-align: left;">

<button class="info" name="_Server_" value="_SERVER_allservers_">
<img src="'$SERVERICON2'" alt="'$"All Servers"'">
<span>'$"All Servers"'</span>
</button>
<br>'$"All Servers"'</td>'
echo '</tr></tbody></table></div></form></div></body></html>'

exit
