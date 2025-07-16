@echo off
echo Starting Conversational Browser Control Agent with Guided Conversation Flow...
echo.
echo This version implements a step-by-step guided conversation for email automation
echo similar to the conversation flow you described, collecting credentials within
echo the conversation rather than in the sidebar.
echo.
echo Press Ctrl+C to exit
echo.

cd /d "%~dp0"
streamlit run streamlit_app_guided.py
