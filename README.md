# MS Team Class joiner
python project for joining classes on time<br />
 
# How to use
simply replace images with there counterpats at that time using snipping tool (win+shift+s)<br />
edit Timetable.json with, class scheduled or not(bool), subject code,teacher name, start time, end time, row and column number for the team
 

"time": [          <--------Block containing times for different classes <br />
  {<br />
    "ID": 0,       <--------ID for the cell<br />
    "class": 1,    <--------Class ID<br />
    "name": "CSE", <--------Class name<br />
    "t-name": "",  <--------Teacher's name<br />
    "start": 915,  <--------Class start time<br />
    "end": 1015,   <--------Class end time<br />
    "number": 4,   <--------Collumn number for the team (starts form 0)<br />
    "row": 0       <--------Row number for the team (starts form 0)<br />
  },<br />
