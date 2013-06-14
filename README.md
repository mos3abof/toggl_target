Toggl Target
============

At work, we track our working hours on Toggl (www.toggl.com), so I created this small project to calculate how many hours I should work to achieve my monthly goals.

You will need to install `requests` and `dateutil` python libraries to be able to use this.


Intallation on linux
--------------------

If you are using linux, you most probably have Python already installed on your machine. 
If not, use your distro's package management system to install Python 2.7

* Downloading the source code from [here](https://github.com/mos3abof/toggl_target/archive/master.zip)
* navaigate to the directory and run the following command to install the required packages :

```
$ pip install -r requirements.txt
```

* Rename `config.py-example` to `config.py` and edit the values in it. Your Toggl  API token can be found in your Toggl account's settings.

Installation on Windows
-----------------------

* If you don't have Python installed, then you must install Python 2.7 from [here](http://python.org/ftp/python/2.7.5/python-2.7.5.msi)
* Download the file
* Press the start button, select run, and run cmd.exe
* In the command shell, run these commands

```
python distribute_setup.py
easy_install pip
pip install python-dateutil requests
```

* Download toggl_target from [here](https://github.com/mos3abof/toggl_target/archive/master.zip)
* Expand the downloaded zip file, copy `config.py-example` & paste it as `config.py` beside `run.py`
* Change your API key in `config.py` Your Toggl  API token can be found in your Toggl account's settings.
* Run `python run.py`

Usage
-----

To use the script run the following command :

```
$ python run.py
```

The output will be something like :

```
Hi
Checking Internet connectivity...
Internet seems fine!

I am trying to connect to Toggl, hang on!

So far you have tracked 15.65 hours

Business days left till deadline : 18
Total days left till deadline : 26

Rquired working hours for this month : 176

To achieve the minimum :
    you should log 7.93 hours every business day 
    or log 5.49 hours every day

To achieve the required :
    you should log 8.91 hours every business day 
    or log 6.17 hours every day

So far you have achieved 8.89 % of your target
```

Authors and Contributores
-------------------------

In June 2013, @mos3abof (http://www.mos3abof.com) started this project and had plenty of help and guidance from @mtayseer (http://www.mtayseer.net).


Support or Contact
------------------
If you have trouble using this code, your can contact toggl@mos3abof.com and I’ll help you sort it out if I have enough time :).



Bug Reports & Feature Requests
------------------------------

To report bugs, issues or feature requests please use the Issues Queue on this Github repository to make it easier for me to maintain. Please don't send those to my email.



License
-------

```
This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 2 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.
```
