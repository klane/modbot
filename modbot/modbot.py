import os
import sys

import dotbot

from modbot import HOME, LOG
from modbot.config import Config


def add(config, filename, target=None):
    config = Config(config) if type(config) is not Config else config
    path, filename = os.path.split(filename)

    if not path:
        path = os.getcwd()

    if target is None:
        target = filename

    target_path, target = os.path.split(target)

    if not target_path:
        target_path = config.path
    elif config.path not in target_path:
        target_path = os.path.join(config.path, target_path)

    filename = os.path.join(path, filename)
    target = os.path.join(target_path, target)

    if not os.path.isfile(filename):
        LOG.error('File does not exist')
        exit(1)

    if os.path.isfile(target):
        LOG.error('File already linked')
        exit(1)

    config.add_link(filename.replace(HOME, '~'), target)
    config.save()

    LOG.info('Moving {1} from {0} to {2}'.format(*os.path.split(filename), target_path))
    os.rename(filename, target)
    run_dotbot(config.file)


def remove(config, filename):
    config = Config(config) if type(config) is not Config else config
    link = config.remove_link(filename)
    config.save()

    LOG.info('Moving {1} to {0}'.format(*os.path.split(link)))
    os.remove(link)
    os.rename(filename, link)
    run_dotbot(config.file)


def run_dotbot(config_file):
    sys.argv[1:] = ['--config-file', config_file]
    dotbot.main()
