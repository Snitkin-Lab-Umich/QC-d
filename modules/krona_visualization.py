__author__ = 'alipirani'
import os
from config_settings import ConfigSectionMap
import subprocess
from modules.log_modules import keep_logging
from logging_subprocess import *

def krona_visualization(kraken_out, Config, logger, kraken_directory, cluster):
    keep_logging("", "Preparing Krona Input file from Kraken results...", logger, 'info')
    prepare_krona_input = "cut -f2,3 %s_kraken > %s_krona.input" % (kraken_out, kraken_out)
    keep_logging('', prepare_krona_input, logger, 'debug')
    krona_cmd = "%s %s_krona.input -o %s_krona.out.html" % (ConfigSectionMap("krona", Config)['base_cmd'], kraken_out, kraken_out)
    keep_logging('', krona_cmd, logger, 'debug')
    cmd = ""
    if cluster == "local":
        call(prepare_krona_input, logger)
        call(krona_cmd, logger)
    #os.system(prepare_krona_input)
    cmd = prepare_krona_input + "\n" + krona_cmd
    return cmd
