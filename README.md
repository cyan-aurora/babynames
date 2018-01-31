# Better names for trans people

> Pick a name that gives the statistically least likelihood of indicating that
> you are trans

## How to run

    $ python tnames.py $THE_YEAR_YOU_WERE_BORN

(That's all). If you want to change how many to display (default 10), add
`--display 20` or so.

For the most recent data (not necessary for functioning)

    $ pip install -r requirements.txt
    $ make

Now run with `--now $YEAR` where `$YEAR` is the most recent year in the scrape.

This heavily leverages the
[baby names scrape tool](https://github.com/jsvine/babynames)
created by jsvine.

