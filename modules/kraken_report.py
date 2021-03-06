__author__ = 'alipirani'
import os
import subprocess
from modules.log_modules import keep_logging
from logging_subprocess import *
from config_settings import ConfigSectionMap
from modules.generate_cluster_jobs import *
from modules.run_parallel import *


def kraken_report(filenames_array, Config, logger, output_folder, type, samples, kraken_directory, cluster, scheduler):
    kraken_report_array = []
    echo = "echo \"Sample,Percentage of reads for Species,# of reads for Species, Species\" > %s/Kraken_report_final.csv" % (kraken_directory)
    os.system(echo)
    prepare_report = "for i in %s/*_report.txt; do grep -w \'S\' $i | sort -k1n | tail -n1; done > %s/Kraken_report_temp.txt\npaste %s %s/Kraken_report_temp.txt > %s/Kraken_report_combined.txt\n" \
                             "awk -F\'\\t\' \'BEGIN{OFS=\",\"};{print $1, $2, $3, $7}\' %s/Kraken_report_combined.txt >> %s/Kraken_report_final.csv\n" \
                             "sed -i \'s/\\s//g\' %s/Kraken_report_final.csv" % (kraken_directory, kraken_directory, samples, kraken_directory, kraken_directory, kraken_directory, kraken_directory, kraken_directory)
    subprocess.call(prepare_report, shell=True)

    keep_logging('', prepare_report, logger, 'debug')
    keep_logging('',
                 "\nKraken Report - %s/Kraken_report_final.csv" % kraken_directory, logger, 'debug')


    # for file in filenames_array:
    #     file_prefix = kraken_directory + "/" + os.path.basename(file)[0:20]
    #     kraken_out = file_prefix + "_kraken"
    #     report_cmd = "kraken-report --db %s %s > %s_report.txt" % (ConfigSectionMap("kraken", Config)['db_path'], kraken_out, kraken_out)
    #     keep_logging(report_cmd, report_cmd, logger, 'debug')
    #     if cluster == "cluster":
    #         generate_cluster_jobs(report_cmd, file_prefix, scheduler, Config, logger)
    #     elif cluster == "parallel-local":
    #         kraken_report_array.append(report_cmd)
    #     elif cluster == "local":
    #         call(report_cmd, logger)
    # if cluster == "parallel-local":
    #     #complete = run_parallel(kraken_report_array)
    #     prepare_report = "for i in %s/*_report.txt; do grep -w \'S\' $i | sort -k1n | tail -n1; done > %s/Kraken_report_temp.txt\nls %s/*_report.txt > %s/filenames\npaste %s/filenames %s/Kraken_report_temp.txt > %s/Kraken_report_combined.txt\n" \
    #                          "awk -F\'\\t\' \'BEGIN{OFS=\",\"};{print $1, $2, $3, $7}\' %s/Kraken_report_combined.txt >> %s/Kraken_report_final.csv" % (kraken_directory, kraken_directory, kraken_directory, kraken_directory, kraken_directory, kraken_directory, kraken_directory, kraken_directory, kraken_directory)
    #
    #     subprocess.call(["for i in %s/*_report.txt; do grep -w 'S' $i | sort -k1n | tail -n1; done > %s/Kraken_report_temp.txt" % (kraken_directory, kraken_directory)], shell=True)
    #     print "for i in %s/*_report.txt; do grep -w 'S' $i | sort -k1n | tail -n1; done > %s/Kraken_report_temp.txt" % (kraken_directory, kraken_directory)
    #     os.chdir(kraken_directory)
    #     subprocess.call(["ls *_report.txt > %s/filenames" % (
    #                         kraken_directory)], shell=True)
    #     subprocess.call(["paste %s/filenames %s/Kraken_report_temp.txt > %s/Kraken_report_combined.txt" % (kraken_directory, kraken_directory, kraken_directory)], shell=True)
    #     subprocess.call(["awk -F'\t' 'BEGIN{OFS=\",\"};{print $1, $2, $3, $7}' %s/Kraken_report_combined.txt >> %s/Kraken_report_final.csv" % (kraken_directory, kraken_directory)], shell=True)
    #
    #     #print "Running:\n%s" % prepare_report
    #     keep_logging('', prepare_report, logger, 'debug')