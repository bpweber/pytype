# A CLI typing test written in Python

> [!NOTE]
> Word list is from [here](https://gist.github.com/deekayen/4148741)

Launch with `python main.py <args>`

Available args:

`-diff=<1-10>` what percentage of the total list of words to use to generate phrases

`-len=<1-50>` how many words are in each phrase

`-caps` capitalizes first word of each phrase

`-punc` adds punctuation to phrase

`-noclear` leaves each line in terminal after enter is pressed


Use a `KeyboardInterrupt`, `Ctrl+C` by default, to end the test and view average stats for that test
