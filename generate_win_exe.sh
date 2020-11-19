#!/bin/bash

pyinstaller --onefile downloader/app.py
mv dist/app.exe dist/downloader.exe
