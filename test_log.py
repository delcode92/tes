import logging
from debug import Debug
from errinfo import ErrInfo

debug2 = Debug(write_file=True)
# err_info = ErrInfo()

# print("=====================================")
# print("this just info in dev/production ....")

debug = Debug(write_file=False)
debug.debugMSG("This is a debug message in dev....")

# print("=====================================\n\n")

debug2.infoMSG("This is an info message put in log file.")
debug2.errMSG("This is an info message put in log file.")
# err_info.errMSG("This is an error message.")

# err_info.infoMSG("This is an info message put in log file.")
# err_info.errMSG("This is an error message.")

