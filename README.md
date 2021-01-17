# GarbageBot-Framework-


## Introduction
I built this project out of boredom. This project is an unofficial Web WhatsApp API and will be supported as of when I am or accept pulls. The older version is broken due to WhatsApp Web so this has been reconstructed to make it easier to use. My old project was during my 11th and 12th grade and as such shows my inexperience as a programmer. I believe this code is a better design, though the commenting is bad. The project builds on 3 WhatsApp projects. Though one of them seems to have been removed from Github. The other 2 are:

1) [Simple-Yet-Hackable-WhatsApp-api by VISWESWARAN1998](https://github.com/VISWESWARAN1998/Simple-Yet-Hackable-WhatsApp-api)
2) [WaWebSessionHandler by jeliebig](https://github.com/jeliebig/WaWebSessionHandler)

## Usage

### API
```python
from Core import API

#log_levels = {"info": 20,"debug": 10,"warning": 30,"error": 40,"critical": 50,"null": 0}
#browsers = {"chrome": webdriver.Chrome,"firefox": webdriver.Firefox,"edge": webdriver.Edge,"opera": webdriver.Opera,safari": webdriver.Safari}
#profile_filename is the cofiguration of web whatsapp. Based on https://github.com/jeliebig/WaWebSessionHandler
api = API(browser,profile_filenmae,log_level)
api.typer("<Message to be set>",api.chat_textbox())
api.send("<Path Of File>","<Caption>")
```

### Bot
```python
from Bot import Bot

#log_levels = {"info": 20,"debug": 10,"warning": 30,"error": 40,"critical": 50,"null": 0}
#browsers = {"chrome": webdriver.Chrome,"firefox": webdriver.Firefox,"edge": webdriver.Edge,"opera": webdriver.Opera,safari": webdriver.Safari}
#profile_filename is the cofiguration of web whatsapp. Based on https://github.com/jeliebig/WaWebSessionHandler
#bot_name is the name you want to give it
#command_prefix is the symbol before the command
#db is database for users storage.
def foo(bot):
    return bot.typer("foo",bot.textbox)
bot = Bot(bot_name,command_prefix,browser,profile_file,log_level,db)
bot.add_command("<Name of Function>","Description of Function",foo)
bot.add_commands({"<Name of Function>":["<Description>",foo]})
#OR bot.add_commands({"<Name of Function>":{"desc": "<Description>","func": foo]})
bot.remove_command("<Name of Function>")
bot.remove_commands(["<Name of Function>"])
bot.start() # Starts loop for commands

```

## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

Please make sure to update tests as appropriate.

## Notes

1) Not sure why Chrome headless mode doesn't work... I am as curious as everyone else.
2) Not sure how to impliment Edge when Edge is weird in selenium
3) Not Supported PhatomJS and Internet Explorer (Who are you who uses IE?)
4) Please tell me if how to improve if you find something to improve on.

## License
[MIT](https://choosealicense.com/licenses/mit/)

