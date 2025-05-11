App to generate helpful trail metrics based on data collected by trail counters.

Authored by Timmy Boyce.

Hope you have as much fun using this app as I had building it, though if you have that
much fun just looking over trail data you may be crazy.

If you are a CS person or Pete Pettengill somehow roped some other person into building
him a new app, feel free to clone this repo or use any of its code.


Limitations (may be fixed eventually if I get really bored one day):

Multiple configs with bar graph does not work how it should. Bar graph is best used
with one config at a time.

When comparing date ranges, sometimes dates don't line up and graph looks weird.

When comparing totals and different sizes of date ranges such as jan 2018-dec 2018
and jan 2019-april-2019, because one is less time, the totals for the other will
be much higher. Ideally you would be required to keep the date ranges equally spaced
but that isn't implemented yet.

Files have to be mostly in the format of the Trafx counters, and are at least
expected to have a line starting with =START which is used to determine when the
counter was set up.

No help page yet, just a reference to this file. If you're here from that useless
help screen, hello! I'll get it done someday. Hope you didn't come here with too
high expectations because this isn't that helpful either, but hopefully the app is
intuitive enough anyways.


Email timmy.m.boyce@gmail.com with any questions or ideas for improving the app
(other than the ones above that I don't feel like fixing yet) and I will try to
implement them ASAP!
