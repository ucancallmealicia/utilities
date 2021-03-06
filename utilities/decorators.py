#/usr/bin/python3
#~/anaconda3/bin/python

import functools, utilities, logging, time

# def keeptime(func):
#     pass
#
# def backups(func):
#     pass

def loopit(func):
    """A decorator that wraps a for loop."""
    @functools.wraps(func)
    def wrapper(grid, *args, **kwargs):
        for row_num, i in enumerate(grid, 1):
            func(i, *args, **kwargs)
        return row_num
    return wrapper

def time_it(func):
    """a decorator that times the execution of a function"""
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        elapsedtime = time.time() - start_time
        m, s = divmod(elapsedtime, 60)
        h, m = divmod(m, 60)
        print('Total time elapsed: ' + '%d:%02d:%02d' % (h, m, s) + '\n')
        return result
    return wrapper

def keeptime(start):
    """Calculates how long a function takes to run. Have to initiate
    the start time at the beginning of the function its used in.

    TODO: Wrapper function"""
    elapsedtime = time.time() - start
    m, s = divmod(elapsedtime, 60)
    h, m = divmod(m, 60)
    logging.debug('Total time elapsed: ' + '%d:%02d:%02d' % (h, m, s) + '\n')

#ADD TO TESTS FOR DECORATORS
# @loopit
# def iterate_me(csvfile, api_url=None, headers=None):
#     uri = csvfile[0]
#     title = csvfile[1]
#     record_json = requests.get(api_url + uri, headers=headers).json()
#     if 'title' in record_json:
#         record_json['title'] = title
#     record_post = requests.post(api_url + uri, headers=headers, json=record_json).json()
#     print(record_post)
#
# def error_log(filepath=None):
#     if filepath != None:
#         logger = filepath
#     else:
#         if sys.platform == "win32":
#             logger = '\\Windows\\Temp\\error_log.log'
#         else:
#             logger = '/tmp/error_log.log'
#     logging.basicConfig(filename=logger, level=logging.DEBUG,
#                         format='%(asctime)s %(levelname)s %(name)s %(message)s')
#     return logger

#still don't totally get how this works
#https://www.blog.pythonlibrary.org/2016/06/09/python-how-to-create-an-exception-logging-decorator/
def exception(logger):
    """
    A decorator that wraps the passed in function and logs
    exceptions should one occur
    """
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            logger = utilities.error_log()
            try:
                return func(*args, **kwargs)
            except:
                # log the exception
                err = "There was an exception in  "
                err += func.__name__
                logging.exception(err)
                # re-raise the exception
                raise
        return wrapper
    return decorator
