Toggl Target
============

[![Codacy Badge](https://api.codacy.com/project/badge/Grade/6cc811c7d497451486079451ec0fbeb6)](https://app.codacy.com/app/mosab-a-ibrahim/toggl_target?utm_source=github.com&utm_medium=referral&utm_content=mos3abof/toggl_target&utm_campaign=badger)

At work, we track our working hours on Toggl (www.toggl.com), so I created this small project to calculate how many hours I should work to achieve my monthly goals.

You will need to install `requests` and `dateutil` python libraries to be able to use this.


Installation on linux
---------------------

If you are using linux, you most probably have Python already installed on your machine.
If not, use your distro's package management system to install Python 2.7

* Download and extract the source code from [here](https://github.com/mos3abof/toggl_target/archive/master.zip)
* Navigate to the extracted directory and run the following command to install the required packages :

```
$ pip install -r requirements.txt
```

* Copy `config.py-example` to `config.py`
* In `config.py` add your Toggl API token, which can be found in your Toggl account's settings.
* Change other values in `config.py` to match your case

Installation on Windows
-----------------------

* If you don't have Python installed, then you must install Python 2.7 from [here](http://python.org/ftp/python/2.7.5/python-2.7.5.msi)
* Open the Windows command shell
* In the command shell, run the following commands

```
python distribute_setup.py
easy_install pip
pip install python-dateutil requests
```

* Download toggl_target from [here](https://github.com/mos3abof/toggl_target/archive/master.zip)
* Extract the downloaded zip file, copy `config.py-example` & paste it as `config.py` beside `run.py`
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

Trying to connect to Toggl, hang on!

So far you have tracked 120.00 hours

Business days left till deadline : 7
Total days left till deadline : 10

Required working hours for this month : 170

To achieve the minimum :
    you should log 4.00 hours every business day
    or log 3.00 hours every day

To achieve the required :
    you should log 7.00 hours every business day
    or log 5.0 hours every day

So far you have achieved:

70.59% [=================================================--------------|------]
```

You can also filter by workspace name's (-w / --workspace), client's name (-c / --client) or project's name (-p / --project), using the following command :

```
$ python run.py -w Work
```

Optionally, you can choose a number of days (-d / --days) left to reach your target, and see the remaining number of hours per day, using the following command :

```
$ python run.py -w Work -d 10
```

Contributores
-------------

* [@mos3abof](http://www.mos3abof.com)
* [@mtayseer](http://www.mtayseer.net)


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
