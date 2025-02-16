#!/bin/bash

pyinstaller --noconsole --onefile app.py
mv dist/app.exe dist/downloader.exe
