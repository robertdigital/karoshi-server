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

SERVERICON="/images/submenus/system/computer.png"
source /opt/karoshi/server_network/domain_information/domain_name
############################
#Show page
############################
echo "Content-type: text/html"
echo ""
echo '

<!DOCTYPE html>
<html>
<head><meta http-equiv="Content-Type" content="text/html; charset=utf-8"><title>'$"Apply SSL Certificate"'</title><meta http-equiv="REFRESH" content="'$TIMEOUT'; URL=/cgi-bin/admin/logout.cgi"><link rel="stylesheet" href="/css/'$STYLESHEET'?d='`date +%F`'"><script src="/all/stuHover.js" type="text/javascript"></script></head><body onLoad="start()"><div id="pagecontainer">'
#Generate navigation bar
/opt/karoshi/web_controls/generate_navbar_admin
echo '<form action="/cgi-bin/admin/apply_ssl_certificate.cgi" name="selectservers" method="post"><b></b>
  <div id="actionbox"><table class="standard" style="text-align: left;" ><tbody><tr>
<td style="vertical-align: top;"><div class="sectiontitle">'$"Apply SSL Certificate"'</div></td><td>
<a class="info" target="_blank" href="http://www.linuxschools.com/karoshi/documentation/wiki/index.php?title=SSL_Certificate"><img class="images" alt="" src="/images/help/info.png"><span>'$"This will create an ssl certificate signed by the root signing authority on your server."' '$"Your client computers will need to have the root signing authority installed into their web browsers."'</span></a></td></tr></tbody></table>
  <br><table class="standard" style="text-align: left;" >
    <tbody>
<tr><td style="width: 180px;"><b>Server</b></td><td style="width: 300px;"><b>Alias</b></td></tr>
<tr><td>'$HOSTNAME'</td><td>manage.'$REALM'</td><td style="width: 90px; vertical-align: top; text-align: left;">
<input name="_SERVER_'$HOSTNAME'_" type="submit" class="button" value="'$"Apply Certificate"'">
</td></tr>
<tr><td>'$"All Web Servers"'</td><td>*.'$REALM'</td>
<td style="vertical-align: top; text-align: left;">
<input name="_SERVER_allwebservers_" type="submit" class="button" value="'$"Apply Certificate"'">
</td></tr></tbody></table>
'


exit

