@echo off
set CUDNN_LIB=C:\Users\22414\cudnn_stub
cd C:\Users\22414\Desktop\agri-paper\tools\rust_llm_poc
C:\Users\22414\Desktop\agri-paper\tools\rust_llm_poc\target\release\eval.exe --offset 0 --limit 80 > C:\Users\22414\Desktop\agri-paper\w4\research\eval_runner.log 2>&1
