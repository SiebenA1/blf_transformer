@echo off
rem create email layout for ticket to IAV blf_converter Service Desk
rem !!! NOT FOR USER - SYSTEM PART

title IAV blf_converter Service Desk - Error Report Mail

set ADDRESS=support+cn-tv-a-toolchain-pre-processing-blf-converter-17733-issue-@gitlab.iav.com
set LINE=//--------------------------------------
set NL=%%0D%%0A
set WS=%%20

color 47
echo.
echo %LINE%
echo // Send error report mail to IAV blf_converter Service Desk
echo // %ADDRESS%
echo //
echo // !!! INTERNET CONNECTION REQUIRED !!!
echo // !!! DO NOT CHANGE THE SYNTAX AND FORMATTING !!!
echo %LINE%
echo.
color 07

start mailto:%ADDRESS%?subject=[blf_converter][ErrorReport]%WS%Topic%WS%(modify)%WS%-%WS%brief%WS%(modify)^
&body="#%WS%problem%WS%description:%NL%%NL%%NL%#%WS%software%WS%version:%NL%%NL%%NL%#%WS%priority:%NL%%NL%%NL%#%WS%contact:%NL%%NL%%NL%"^
"#%WS%input%WS%data%WS%(optionally):%NL%%NL%%NL%#%WS%comment%WS%(optionally):%NL%%NL%%NL%#%WS%proposed%WS%solution%WS%(optionally):%NL%%NL%%NL%"
pause
