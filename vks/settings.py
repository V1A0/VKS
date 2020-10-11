"""
        THIS IS MAIN SETTINGS FILE
Enter here your API token and targets ids
"""

API_TOKEN = '__ENTER_YOUR_VK_API_TOKEN_HERE__'

TARGETS = [
    '123', '23456'
]



"""
                      ADVANCED SETTINGS
(proxy, random proxy mode, debug mode, requests frequency, other)
"""

PROXY = {
    "http": "",
    "https": "",
    "ftp": ""
}

REQ_FREQUENCY = 60

LOG_FILE_NAME = "vks.log"
LOG_MODE = "DEBUG"
MAX_LOG_FILE_SIZE = "10Mb"
COMPRESSION = "zip"

GREETING_ART = """
                 #%%%%%%%%%%%
            ,%%%%%#         %%%%%%
          %%%%%%               %%%%%
        %%%%%%%                  %%%%%
      ,%%%%%%%                    %%%%%%         %%%      %%  %%%  %%%  /%%%%%%%
      %%%%%%%%                    %%%%%%.         %%%    %%#  %%%%%%    %%%.
     %%%%%%%%%       %%%  %%%   %%%%%%%%%          %%%  %%%   %%%%%       %%%%%
     %%%%%%%%%%       %%% %%% %%%%%%%%%%%           %%%%%%    %%%%%%          %%%
     %%%%%%%%%%%       %%%%% %%%(%%%%%%%%            %%%%%    %%%  %%%  %    %%%%
      %%%%%%%%% %              %%%%%%%%%             %%%%     %%%   %%% %%%%%%%/  v0.2
       %%%%%%    %%*         ,%%%%%%%%%
        %%%%%        %%%%*  %%%%%%%%%%
          /%%%%             %%%%%%%%
              %%%%%%%%%%%%%%%%%%
                     %%%%
"""

"""==================================================================================================
                                    DON'T TOUCH ANYTHING DOWN HERE
=====================================================================================================                         
"""

"""Set log settings
loguru.loger.add(*args, **kwargs)
"""
logger.add(LOG_FILE_NAME, level=LOG_MODE, rotation=MAX_LOG_FILE_SIZE,
           compression=COMPRESSION
           )


"""Converting targets list to string
['123', '456', '789'] to "123,456,789"
"""
temp_ = ''
for target in TARGETS:
    temp_ += ',' + str(target)

TARGETS = temp_[1:]

