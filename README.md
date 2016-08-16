# ohio-2016-primary-d-to-r

![ohio-2016-primary-d-to-r](http://i.imgur.com/JdK67AO.png)

When voting in a primary election in Ohio, one must request a party-specific ballot. John Kasich won the 2016 Ohio Republican primary; it was the only state he won. It had been widely speculated that many Ohio voters who would normally vote in the Democratic primary opted to vote in the Republican primary in order to defeat Donald Trump.

This script is designed to estimate how many Ohio Republican primary voters switched in 2016. It parses the voter data provided by the [Ohio Secretary of State](http://www.sos.state.oh.us/SOS/elections/Research/electResultsMain/2016Results.aspx).

### Method

The script works by collecting all of the voters who requested a Republican ballot. Then it checks their voting history, dating back to 2000. If they requested a Democratic ballot in the last primary (for any office) they participated in (prior to 2016), that is considered a switch.

#### Deviation from Ohio Secretary of State

The Ohio Secretary of State [released their own calculations](http://www.sos.state.oh.us/sos/mediaCenter/2016/2016-05-18.aspx) for this Democrat-to-Republican switch. Their count comes in to about _half_ of what this script finds. That's because Ohio considers you "unaffiliated" if you haven't voted in _any_ primary for _any_ office across the last 3 primary cycles. So, for example, if you only vote in Presidential primaries, but missed 2012, you became "unaffiliated". I believe this is overzealous pruning.

## Usage

```sh
git clone git@github.com:hodgesmr/ohio-2016-primary-d-to-r.git ~/ohio-2016-primary-d-to-r
python ~/ohio-2016-primary-d-to-r/analyze.py
```

The script will download, parse, and analyze the voter data from all Ohio counties. It will output the "switch" data to a timestamped directory in `~/ohio-2016-primary-d-to-r/data/`.

## A Matt Hodges project

This project is maintained by [@hodgesmr](http://twitter.com/hodgesmr).

_Please use it for good, not evil._
