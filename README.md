# Security Benchmarking Tool

This application allows you to parse the local `.audit` files related to [tenable policies](https://www.tenable.com/downloads/download-all-compliance-audit-files) and to store it into `.json` file and after that to convert it into a database.

## Technologies

* [Python 3.8.2](https://www.python.org/downloads/release/python-382/)
* [tkinter](https://docs.python.org/3/library/tkinter.html)
* [Sqlite 3.31.1](https://www.sqlite.org/releaselog/3_31_1.html)

## GUI

The Graphical User Interface is implemented in project using [tkinter](https://docs.python.org/3/library/tkinter.html).
## To Use

Firstly, clone this repository using [Git](https://git-scm.com) or download `.zip` archive with project.  
Secondly, you will need to install [Sqlite3](https://www.sqlite.org/releaselog/3_31_1.html) using this command: `pip3 install sqlite3`.  
After that, `cd` into the folder with project and run `python app.py`  
The application will start and you will be able to manipulate it by GUI. 
