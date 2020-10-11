# youtube-live-translate-chat-collector
When I am watching Hololive there will be some guy translate with start message with'[EN]' so I decide to collect it for reading
Using [pytchat]

## how to use

### 5 steps to go:
1) "pip install pytchat" or "python -m pip install pytchat"
2) copy my code and run it
3) put link as "https://www.youtube.com/watch?v=aaaaaaaaaaaa" or id like "aaaaaaaaaa" to shell and press enter
4) check your clip what translator will always translate as, and add case/sensitive case in condition()
5) enjoy~~

### What command you can add to shell:
> after you put link in python shell you will be able to modify collector using this program python shell
 * link:(new link)              : to change current collecting outube link
 * toggle auto                  : there are auto collect  " : "   with somecondition if it doesn't work out well you should use this command
 * print all                    : print all object that adjustable
 * eval: smt                    : to erun smt in program such as eval:print(maintranslator)
 * exit                         : to exit
 * 'smt' add  keyword/member    : add 'smt' to keyword if there are 'smt' in sender message, it will show up on screen
 * 'smt' remove keyword/member  : remove 'smt' from keyword
 * 'smt' add/remove blockkeyword/blockmember : default for blockkeyword is '[ES]' for avoid catchin "[ES]:" or espanish translate
 
### After program end
 It will show who has the most translate 
 Press Enter to exit

> thx for using my code~

## some addition detail

### Test type:
there are 4 test type
If you don't like my main version you can use another version in [testtype folder]

If you don't have a video to test ther will always be translator on sheep chanel.Try it there!

PS: case sensitive that I have founded and add to my code
[en] [eng] [EN] [ENG] 【en】【eng】(en) (eng) [(smth)/en]([英訳/EN]) or "she is talking about something" ore even with out[en] but use "she:smth" instead...


[pytchat]:<https://github.com/taizan-hokuto/pytchat>
[testtype folder]:<https://github.com/fah-OwO/youtube-live-translate-chat-collector/blob/master/testtype>
