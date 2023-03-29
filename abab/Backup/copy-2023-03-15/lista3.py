from datetime import datetime, date
import os
import shutil


def backup(ext, directories):
    """
    Tworzy kopię zapasową podanych katalogów.

    :param ext: rozszerzenie
    :param directories:
    :return: None
    """
    '''
     if destination == ' ':
        destination = os.getcwd()
    if type(directories) != tuple and list:
        actual_directories = (directories,)
    else:
        actual_directories = directories
    for directory in actual_directories:
        with zipfile.ZipFile(str(destination) + '/' + str((date.today())) + ' ' + str(directory) + '.zip', 'w') as zip_file:
            for file in os.scandir(str(directory)):
                zip_file.write(file)'''
    if type(directories) != tuple and list:
        actual_directories = (directories,)
    else:
        actual_directories = directories
    name = '/Users/tomasz/PycharmProjects/programowanie/Backup/copy-'+str(date.today())
    os.makedirs(name, exist_ok=True)
    # with open(name, mode='w') as direc:
    for directory in actual_directories:
        for file in os.listdir(str(directory)):
            ts = os.path.getmtime(file)
            duration = datetime.now() - datetime.fromtimestamp(ts)
            duration_in_days = duration.total_seconds()/259200
            print(str(file))
            if duration_in_days < 3 and str(file).endswith(str(ext)):
                shutil.copy(file, name)


backup('.py', '/Users/tomasz/PycharmProjects/programowanie')
