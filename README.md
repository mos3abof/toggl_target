Toggl Target
============

At work, we track our working hours on Toggl (www.toggl.com), so I created this small project to calculate how many hours I should work to achieve my monthly goals.

You will need to install `requests` and `dateutil` python libraries to be able to use this.

To get started, rename `config.py-example` to `config.py` and edit the values in it. 

Your Toggl  API token can be found in your account's settings.


A sample output looks like this :

```
>>> python ~/dev/toggl_target/toggl_target.py 
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
