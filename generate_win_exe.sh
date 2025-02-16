#!/bin/bash

pyinstaller --onefile app.py
mv dist/app.exe dist/downloader.exe
