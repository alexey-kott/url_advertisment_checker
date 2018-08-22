from urllib.parse import quote_plus

import requests as req

url = 'https://ru.megaindex.com/a/tcategories?domain=https://personhunters.com'

response = req.get(f'https://api.proxycrawl.com/?token=jbzJeTVyoiUlgSKZsyO3eQ&url={url}')

with open("response.html", "w") as file:
    file.write(response.text)