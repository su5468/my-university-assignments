#! python
import re

with open("probelm2.html", "rt", encoding="utf-8") as f:
    text = f.read()
    mails = re.findall(
        r'''<b>E-mail</b>
                	<br/>
                	<a href="mailto:(.+?)"''',
        text,
    )
    phones = re.findall(
        r"""<b>전화번호:</b>
                	(.+?)
                </dd>""",
        text,
    )
    sites = re.findall(
        r'''<b>홈페이지:</b>
                	<a href="(.+?)"''',
        text,
    )

print(f'E-mail: {", ".join(mails)}\n')
print(f'Phone Number: {", ".join(phones)}\n')
print(f'HomePage: {", ".join(sites)}\n')
