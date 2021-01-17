import os
def test_picture(bot):
    bot.send(os.getcwd() + "\\Temp\\selenium-python.png","This is a test")
def test_text(bot):
    bot.typer(' '.join(bot.message.split(' ')[1:]),bot.textbox)