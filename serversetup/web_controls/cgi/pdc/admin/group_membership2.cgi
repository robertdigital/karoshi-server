#!/bin/bash
#Copyright (C) 2012 Paul Sharrad

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

########################
#Required input variables
########################
#  _USERNAME_

#Detect mobile browser
MOBILE=no
source /opt/karoshi/web_controls/detect_mobile_browser
source /opt/karoshi/web_controls/version

########################
#Language
########################

STYLESHEET=defaultstyle.css
[ -f /opt/karoshi/web_controls/user_prefs/"$REMOTE_USER" ] && source /opt/karoshi/web_controls/user_prefs/"$REMOTE_USER"
export TEXTDOMAIN=karoshi-server

#########################
#Show page
#########################
echo "Content-type: text/html"
echo ""
echo '<!DOCTYPE html><html><head><meta http-equiv="Content-Type" content="text/html; charset=utf-8"><title>'$"Group Membership"'</title><link rel="stylesheet" href="/css/'"$STYLESHEET"'?d='"$VERSION"'"></head><body><div id="pagecontainer">'
#########################
#Get data input
#########################
DATA=$(cat | tr -cd 'A-Za-z0-9\._:\-%*+-' | sed 's/___/TRIPLEUNDERSCORE/g' | sed 's/_/UNDERSCORE/g' | sed 's/TRIPLEUNDERSCORE/_/g')
#########################
#Assign data to variables
#########################
END_POINT=15
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

#Assign USERNAME
DATANAME=USERNAME
get_data
USERNAME="$DATAENTRY"

#Assign ACTION
DATANAME=ACTION
get_data
ACTION="$DATAENTRY"

#Assign GROUP
DATANAME=GROUP
get_data
GROUP="${DATAENTRY//UNDERSCORE/_}"

function show_status {
echo '<SCRIPT language="Javascript">
alert("'"$MESSAGE"'");
window.location = "/cgi-bin/admin/group_membership_fm.cgi"
</script>
</div></body></html>'
exit
}
#########################
#Check https access
#########################
if [ https_"$HTTPS" != https_on ]
then
	export MESSAGE=$"You must access this page via https."
	show_status
fi
#########################
#Check user accessing this script
#########################
if [ ! -f /opt/karoshi/web_controls/web_access_admin ] || [ -z "$REMOTE_USER" ]
then
	MESSAGE=$"You must be a Karoshi Management User to complete this action."
	show_status
fi

if [[ $(grep -c ^"$REMOTE_USER:" /opt/karoshi/web_controls/web_access_admin) != 1 ]]
then
	MESSAGE=$"You must be a Karoshi Management User to complete this action."
	show_status
fi
Checksum=$(sha256sum /var/www/cgi-bin_karoshi/admin/group_membership2.cgi | cut -d' ' -f1)
#########################
#Check data
#########################
#Check to see that username is not blank
if [ -z "$USERNAME" ]
then
	MESSAGE=$"You have not entered in a username."
	show_status
fi

#Check to see that action is not blank
if [ -z "$ACTION" ]
then
	MESSAGE=$"The action cannot be blank."
	show_status
fi

#Check to see that the action  is correct
if [ "$ACTION" != ADD ] && [ "$ACTION" != REMOVE ]
then
	MESSAGE=$"Incorrect action."
	show_status
fi

#Check to see that group is not blank
if [ -z "$GROUP" ]
then
	MESSAGE=$"The group cannot be blank."
	show_status
fi

#Check to see that the user exists
getent passwd "$USERNAME" 1>/dev/null 2>/dev/null
USEREXISTSTATUS="$?"
if [ "$USEREXISTSTATUS" != 0 ]
then
	MESSAGE=$"This user does not exist."
	show_status
fi

echo "$REMOTE_USER:$REMOTE_ADDR:$Checksum:$USERNAME:$ACTION:$GROUP" | sudo -H /opt/karoshi/web_controls/exec/group_membership2
echo "<form action=\"group_membership.cgi\" method=\"post\" id=\"membershipview\">
<input type=\"hidden\" name=\"____USERNAME____$USERNAME""____\" value=\"\">
</form>
<script language=\"JavaScript\" type=\"text/javascript\">
document.getElementById('membershipview').submit();
</script></div></body></html>"
exit
