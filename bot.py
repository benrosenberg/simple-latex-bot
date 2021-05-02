import discord, os

TOKEN = ### INSERT TOKEN HERE ###

bot = discord.Client()

@bot.event
async def on_ready():
    print(f'Bot connected as {bot.user}')

@bot.event
async def on_message(message):
    if message.author.bot or not message.content[:6] == 'latex ': return
    before_eq_string = r"\documentclass{article}\usepackage[margin=0.1in]{geometry} \usepackage{amsmath} \usepackage{amssymb} \begin{document} \thispagestyle{empty} \setlength{\parindent}{0pt} $$"
    after_eq_string = r"$$ \end{document}"
    tex_file_contents = before_eq_string + message.content[6:] + after_eq_string
    tex_file = open("tempfile.tex", "w")
    tex_file.write(tex_file_contents)
    tex_file.close()
    os.system('pdflatex tempfile.tex > /dev/null 2>&1')   # the '> /dev/null 2>&1' part is a hack to make the command quiet
    os.system('pdfcrop -margin 3 tempfile.pdf tempfile.pdf > /dev/null 2>&1')
    os.system('convert -quiet -density 3000 -background white -alpha remove -alpha off tempfile.pdf -quality 90 tempfile.png')
    os.system('rm tempfile.log tempfile.aux tempfile.pdf tempfile.tex')
    await message.channel.send(file=discord.File('tempfile.png'))

bot.run(TOKEN)
