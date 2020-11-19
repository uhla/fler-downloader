# fler-downloader

Usage: `python3 downloader/app.py <username> <password>`

Downloads list of all selled products from fler.cz and saves them into docx document with main photos, tags, etc. Products are grouped by title (assuming there is multiple variants of the product) and shared description is used.

Apart from export, application allows using customized descriptions for specific products that are unavailable from regular API.
