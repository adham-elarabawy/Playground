#!/bin/bash
@echo off

for /F %%f in (classNames.txt) do (
	powerShell -Command ".\yolo_mark.exe D:\Kelzal\24_class\imgs cap_video D:\Kelzal\24_class\inside_vids\inside_" + %%f + ".mp4 10"
)