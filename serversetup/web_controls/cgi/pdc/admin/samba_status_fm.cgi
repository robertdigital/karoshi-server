#!/bin/bash
#Copyright (C) 2016  Paul Sharrad

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

#Detect mobile browser
MOBILE=no
source /opt/karoshi/web_controls/detect_mobile_browser
source /opt/karoshi/web_controls/version

############################
#Language
############################
SHUTDOWN_CODE=`echo ${RANDOM:0:3}`

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
  <title>'$"Client Connections"'</title><meta http-equiv="REFRESH" content="'$TIMEOUT'; URL=/cgi-bin/admin/logout.cgi">
  <link rel="stylesheet" href="/css/'$STYLESHEET'?d='$VERSION'">
  <script>
<!--
function SetAllCheckBoxes(FormName, FieldName, CheckValue)
{
	if(!document.forms[FormName])
		return;
	var objCheckBoxes = document.forms[FormName].elements[FieldName];
	if(!objCheckBoxes)
		return;
	var countCheckBoxes = objCheckBoxes.length;
	if(!countCheckBoxes)
		objCheckBoxes.checked = CheckValue;
	else
		// set the check value for all check boxes
		for(var i = 0; i < countCheckBoxes; i++)
			objCheckBoxes[i].checked = CheckValue;
}
// -->
  </script>
<script src="/all/stuHover.js" type="text/javascript"></script>
<script src="/all/js/jquery.js"></script>
<script src="/all/js/jquery.tablesorter/jquery.tablesorter.js"></script>
<script id="js">
$(document).ready(function() 
    { 
        $("#myTable").tablesorter(); 
    } 
);
</script>
<meta name="viewport" content="width=device-width, initial-scale=1"> <!--480-->'

if [ $MOBILE = yes ]
then
	echo '<link rel="stylesheet" type="text/css" href="/all/mobile_menu/sdmenu.css">
	<script src="/all/mobile_menu/sdmenu.js">
		/***********************************************
		* Slashdot Menu script- By DimX
		* Submitted to Dynamic Drive DHTML code library: www.dynamicdrive.com
		* Visit Dynamic Drive at www.dynamicdrive.com for full source code
		***********************************************/
	</script>
	<script>
	// <![CDATA[
	var myMenu;
	window.onload = function() {
		myMenu = new SDMenu("my_menu");
		myMenu.init();
	};
	// ]]>
	</script>'
fi

echo '</head><body onLoad="start()"><div id="pagecontainer">'

#Generate navigation bar
if [ $MOBILE = no ]
then
	TOOLTIPCLASS="info"
	DIV_ID=actionbox3
	TABLECLASS=standard
	WIDTH=180
	HEIGHT=20
	#Generate navigation bar
	/opt/karoshi/web_controls/generate_navbar_admin
else
	TOOLTIPCLASS="info infoleft"
	DIV_ID=actionbox2
	TABLECLASS=mobilestandard
	WIDTH=160
	HEIGHT=30
fi

echo '<form action="/cgi-bin/admin/samba_status.cgi" name="selectservers" method="post">'

[ $MOBILE = no ] && echo '<div id="'$DIV_ID'"><div id="titlebox">'

#Show back button for mobiles
if [ $MOBILE = yes ]
then
echo '<div style="float: center" id="my_menu" class="sdmenu">
	<div class="expanded">
	<span>'$"Client Connections"'</span>
<a href="/cgi-bin/admin/mobile_menu.cgi">'$"Menu"'</a>
</div></div><div id="mobileactionbox">'
else
	echo '	<table class="standard" style="text-align: left;" ><tbody>
	<tr><td style="height:30px;"><div class="sectiontitle">'$"Client Connections"' '$SERVER2'</div></td>
	</tr></tbody></table></div><div id="infobox">'
fi

echo '<table class="'$TABLECLASS'" style="text-align: left;" >
    <tbody>
      <tr>
        <td style="width: '$WIDTH'px;">'$"View option"'</td>
        <td style="vertical-align: top; text-align: left;">
	<select name="_OPTION_" style="width: 200px;">
	<option value="connectedusers">'$"Connected Users"'</option>
	<option value="connectedshares">'$"Connected Shares"'</option>
	<option value="openfiles">'$"Open Files"'</option>
	</select>
        <td></td>
      </tr>
</tbody></table><br>
'

#Show list of servers
/opt/karoshi/web_controls/show_servers $MOBILE fileservers $"Select"

[ $MOBILE = no ] && echo '</div>'

echo '</div></form></div></body></html>'
exit