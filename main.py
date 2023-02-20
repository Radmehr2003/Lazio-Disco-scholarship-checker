# coding=utf-8
import config
import logging


# create a logger object for logging
logging.basicConfig(filename="logs.log", level=logging.DEBUG,
                    format='%(asctime)s - %(message)s', datefmt='%d-%b-%y %H:%M:%S')


def sent():

    config.read_data_from_lazio()


sent()