#!/bin/bash
#Copyright (C) 2015  Paul Sharrad

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
<!DOCTYPE html><html><head><meta http-equiv="Content-Type" content="text/html; charset=utf-8">
  <title>'$"Gluster Volume Control"'</title><meta http-equiv="REFRESH" content="'"$TIMEOUT"'; URL=/cgi-bin/admin/logout.cgi">
<link rel="stylesheet" href="/css/'"$STYLESHEET"'?d='"$VERSION"'">
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
if [ "$MOBILE" = yes ]
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

DATA=$(cat | tr -cd 'A-Za-z0-9\._:%\-+*')

#########################
#Assign data to variables
#########################
END_POINT=24
function get_data {
COUNTER=2
DATAENTRY=""
while [[ $COUNTER -le $END_POINT ]]
do
	DATAHEADER=$(echo "$DATA" | cut -s -d'_' -f"$COUNTER")
	if [[ "$DATAHEADER" = "$DATANAME" ]]
	then
		let COUNTER="$COUNTER"+1
		DATAENTRY=$(echo "$DATA" | cut -s -d'_' -f"$COUNTER")
		break
	fi
	let COUNTER=$COUNTER+1
done
}

#Assign VOLUME
DATANAME=VOLUME
get_data
VOLUME="$DATAENTRY"

#Assign ACTION
DATANAME=ACTION
get_data
ACTION="$DATAENTRY"

#Assign SERVER
DATANAME=SERVER
get_data
SERVER="$DATAENTRY"

#Assign SERVERS
DATANAME=SERVERS
get_data
SERVERS="$DATAENTRY"

#Assign FOLDER
DATANAME=FOLDER
get_data
FOLDER="$DATAENTRY"

function show_status {
echo '<SCRIPT language="Javascript">'
echo 'alert("'"$MESSAGE"'")';
echo '                window.location = "/cgi-bin/admin/gluster_control.cgi";'
echo '</script>'
echo "</div></body></html>"
exit
}

[ -z "$ACTION" ] && ACTION=view
ICON1="/images/submenus/system/add.png"
ACTION2=create
ACTIONMSG=$"Create Volume"
if [ "$ACTION" = create ] || [ "$ACTION" = addfolder ] || [ "$ACTION" = assignshare ] || [ "$ACTION" = removefolder ] || [ "$ACTION" = confirmremovefolder ] || [ "$ACTION" = reallyremovefolder ] || [ "$ACTION" = deleteglustervolume ] || [ "$ACTION" = status ] || [ "$ACTION" = restorebrick ]  
then
	ACTION2=view
	ACTIONMSG=$"View Volumes"
	ICON1="/images/submenus/system/gluster.png"
fi
#########################
#Check data
#########################
TITLE="View Volumes"
[ "$ACTION" = create ] && TITLE=$"Create Volume"
[ "$ACTION" = reallycreate ] && TITLE=$"Creating Volume"
[ "$ACTION" = addfolder ] && TITLE=$"Add Folder"
[ "$ACTION" = reallyaddfolder ] && TITLE=$"Ading Folder"
[ "$ACTION" = assignshare ] && TITLE=$"Assign Network Share"
[ "$ACTION" = removefolder ] && TITLE=$"Remove Folder"

if [ "$ACTION" != create ] && [ "$ACTION" != reallycreate ] && [ "$ACTION" != restore ] && [ "$ACTION" != view ] && [ "$ACTION" != addfolder ] && [ "$ACTION" != reallyaddfolder ] && [ "$ACTION" != assignhomefolders ] && [ "$ACTION" != removefolder ] && [ "$ACTION" != reallyremovefolder ] && [ "$ACTION" != confirmremovefolder ] && [ "$ACTION" != deleteglustervolume ] && [ "$ACTION" != status ] && [ "$ACTION" != restorebrick ]
then
	MESSAGE=$"You have not entered a correct action."
	show_status
fi

if [ "$ACTION" = reallycreate ]
then
	if [ -z "$VOLUME" ]
	then
		MESSAGE=$"You have not entered a volume name."
		show_status
	fi
	if [ -z "$SERVERS" ]
	then
		MESSAGE=$"You have not chosen any servers."
		show_status
	fi
	if [[ $(echo "$SERVERS" | sed 's/%2C/,/g' | grep -c ",") = 0 ]]
	then
		MESSAGE=$"You have to choose at least two servers to create a distributed volume."
		show_status
	fi

	if [ -d /opt/karoshi/server_network/gluster-volumes/"$VOLUME" ]
	then
		MESSAGE=''$VOLUME' - '$"This volume has already been created."''
		show_status
	fi
fi

if [ "$ACTION" = reallyaddfolder ]
then
	if [ -z "$VOLUME" ]
	then
		MESSAGE=$"You have not entered a volume name."
		show_status
	fi
	if [ -z "$FOLDER" ]
	then
		MESSAGE=$"You have not chosen a folder path."
		show_status
	fi	
fi

#Generate navigation bar
if [ "$MOBILE" = no ]
then
	DIV_ID=actionbox3
	#Generate navigation bar
	/opt/karoshi/web_controls/generate_navbar_admin
else
	DIV_ID=mobileactionbox
fi



#Show back button for mobiles
if [ "$MOBILE" = yes ]
then
	echo '<div style="float: center" id="my_menu" class="sdmenu"><div class="expanded"><span>'$"Gluster Controls"' '"$SERVER2"'</span></div></div><div id="'"$DIV_ID"'">'
else

	WIDTH=100
	ICON2="/images/submenus/file/folder.png"
	ICON3="/images/submenus/system/network-server.png"

	echo '<div id="'"$DIV_ID"'"><div id="titlebox">


	<div class="sectiontitle">Gluster - '"$TITLE"' <a class="info" target="_blank" href="http://www.linuxschools.com/karoshi/documentation/wiki/index.php?title=Gluster_Volumes"><img class="images" alt="" src="/images/help/info.png"><span>'$"Gluster Volumes"'</span></a></div><form action="/cgi-bin/admin/gluster_control.cgi" method="post">
	<table class="tablesorter"><tbody><tr>

		<td style="vertical-align: top; height: 30px; white-space: nowrap; min-width: '$WIDTH'px; text-align:center;">
			<button class="info infonavbutton" name="_GlusterAction_" value="_ACTION_'"$ACTION2"'_">
				<img src="'$ICON1'" alt="'"$ACTIONMSG"'">
				<span>'"$ACTIONMSG"'</span><br>
				'"$ACTIONMSG"'
			</button>
		</td>

		<td style="vertical-align: top; height: 30px; white-space: nowrap; min-width: '$WIDTH'px; text-align:center;">
			<button class="info infonavbutton" formaction="home_folders_fm.cgi" name="ViewHomeFolders" value="_">
				<img src="'$ICON2'" alt="'$"Home Folders"'">
				<span>'$"Configure user home folders"'</span><br>
				'$"Home Folders"'
			</button>
		</td>

		<td style="vertical-align: top; height: 30px; white-space: nowrap; min-width: '$WIDTH'px; text-align:center;">
			<button class="info infonavbutton" formaction="samba_shares.cgi" name="NetworkShares" value="_">
				<img src="'$ICON3'" alt="'$"Network Shares"'">
				<span>'$"Configure network shares"'</span><br>
				'$"Network Shares"'
			</button>
		</td>

	</tr></tbody></table></form>

	</div><div id="infobox">'
fi

echo '<form action="/cgi-bin/admin/gluster_control.cgi" method="post" id="form1" name="combobox">'
Checksum=$(sha256sum /var/www/cgi-bin_karoshi/admin/gluster_control.cgi | cut -d' ' -f1)
echo "$REMOTE_USER:$REMOTE_ADDR:$Checksum:$ACTION:$VOLUME:$SERVER:$SERVERS:$FOLDER:" | sudo -H /opt/karoshi/web_controls/exec/gluster_control
echo '</form>'

[ "$MOBILE" = no ] && echo '</div>'

echo '</div></div></body></html>'
exit
