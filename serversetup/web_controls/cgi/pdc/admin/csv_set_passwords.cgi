#!/bin/bash
#Copyright (C) 2008 Paul Sharrad

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
#  _PASSWORD1_  Password used for new user
#  _PASSWORD2_  Checked against PASSWORD1 for typos.
#  _GROUP_      This is the primary group for the new user eg yr2000, staff, officestaff.
############################
#Language
############################

STYLESHEET=defaultstyle.css
[ -f /opt/karoshi/web_controls/user_prefs/"$REMOTE_USER" ] && source /opt/karoshi/web_controls/user_prefs/"$REMOTE_USER"
export TEXTDOMAIN=karoshi-server

############################
#Show page
############################
echo "Content-type: text/html"
echo ""
echo '<!DOCTYPE html><html><head><meta http-equiv="Content-Type" content="text/html; charset=utf-8"><title>'$"Set Passwords"'</title><link rel="stylesheet" href="/css/'"$STYLESHEET"'?d='"$VERSION"'"><script src="/all/stuHover.js" type="text/javascript"></script></head><body><div id="pagecontainer">'
#Generate navigation bar
/opt/karoshi/web_controls/generate_navbar_admin
echo '<div id="actionbox3"><div id="titlebox">
<div class="sectiontitle">'$"Set Passwords"'</div></div><div id="infobox">
<br><br>'
#########################
#Get data input
#########################

#DATA=`cat | tr -cd 'A-Za-z0-9\._:\-'`
#GROUP=`echo $DATA | cut -d'_' -f3`

function show_status {

echo '<SCRIPT language="Javascript">
alert("'"$MESSAGE"'")
window.location = "csv_set_passwords_fm.cgi"
</script></div></div></body></html>'
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

if [[ $(grep -c ^$REMOTE_USER: /opt/karoshi/web_controls/web_access_admin) != 1 ]]
then
	MESSAGE=$"You must be a Karoshi Management User to complete this action."
	show_status
fi
#########################
#Check data
#########################
#Check input file
[ -d /var/www/karoshi/csv_set_passwords ] || mkdir -p /var/www/karoshi/csv_set_passwords
chmod 0700 /var/www/karoshi/
chmod 0700 /var/www/karoshi/csv_set_passwords
if [ $(dir /var/www/karoshi/csv_set_passwords --format=single-column | wc -l) != 1 ]
then
	MESSAGE=$"File upload error."
	show_status
fi
CSVFILE=$(ls /var/www/karoshi/csv_set_passwords)
echo >> /var/www/karoshi/csv_set_passwords/"$CSVFILE"
cat /var/www/karoshi/csv_set_passwords/"$CSVFILE" | tr -cd 'A-Za-z0-9\.,_:\-\n\! "#$%&()*+/;<=>?@[\\]^`{|}~' > /var/www/karoshi/csv_set_passwords/"$CSVFILE"2
rm -f /var/www/karoshi/csv_set_passwords/"$CSVFILE"
mv /var/www/karoshi/csv_set_passwords/"$CSVFILE"2 /var/www/karoshi/csv_set_passwords/"$CSVFILE"
sed -i '/^$/d' /var/www/karoshi/csv_set_passwords/"$CSVFILE"
CSVFILE_LINES=$(cat /var/www/karoshi/csv_set_passwords/"$CSVFILE" | wc -l)
Checksum=$(sha256sum /var/www/cgi-bin_karoshi/admin/change_password.cgi | cut -d' ' -f1)
COUNTER=1
while [ "$COUNTER" -le "$CSVFILE_LINES" ]
do
	USERNAME=$(sed -n "$COUNTER,$COUNTER"p /var/www/karoshi/csv_set_passwords/"$CSVFILE" | tr -cd 'A-Za-z0-9_\-,' | cut -s -d, -f1)
	PASSWORD=$(sed -n "$COUNTER,$COUNTER"p /var/www/karoshi/csv_set_passwords/"$CSVFILE" | tr -cd 'A-Za-z0-9\.,_:\-\n\! "#$%&()*+/;<=>?@[\\]^`{|}~' | cut -d, -f2-)
	if [ -z "$USERNAME" ] || [ -z "$PASSWORD" ]
	then
		echo $"Error on line $COUNTER"'<br>'
		MESSAGE=''$"The CSV file you have chosen is not formatted correctly."''
		show_status
	fi
	#Change password expects apache encoding
	PASSWORD=$(urlencode -m "$PASSWORD")
	echo '<ul><li>'"$USERNAME"' - '$"changing password"'</li></ul>'

	#Change password
	echo "$REMOTE_USER:$REMOTE_ADDR:$Checksum:$USERNAME:$PASSWORD:" | sudo -H /opt/karoshi/web_controls/exec/change_password
	let COUNTER="$COUNTER"+1
done
rm -f -R /var/www/karoshi/csv_set_passwords
MESSAGE=$"Set passwords completed."
show_status
echo "</div></div></div></body></html>"
