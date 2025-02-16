# fler-downloader

Usage: `python3 downloader/app.py`

Downloads list of all selled products from fler.cz and saves them into docx document with main photos, tags, etc. Products are grouped by title (assuming there is multiple variants of the product) and shared description is used.

Apart from export, application allows using customized descriptions for specific products that are unavailable from regular API.

# Create windows executable

Create venv based on requirements, then execute from repository root: 

`generate_win_exe.sh`

This will create dist/downloader.exe file that can be executed - this needs to be performed on windows machine for correct executable version.
