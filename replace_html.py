import re
import glob
from pathlib import Path

re_string = r"href\=\"(?P<filename>.{0,})\.html\""
re_replace = r"href\=\"{filename}\.html\""
files = glob.glob("*", root_dir="templates", recursive=True)

for file in files:
    f = Path("templates/" + file)

    text = f.read_text(errors="replace")

    porse = re.findall(re_string, text)

    for filename in porse:
        op = re.sub(re_replace.format(filename=filename), f'href="/{filename}"', text)

        print(op)

        text = op

    f.write_text(text, errors="replace")
