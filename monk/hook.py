import functools


class Hook:

    def __init__(self, after_request=None, before_response=None):
        if after_request is None:
            self.after_request = list()
        if before_response is None:
            self.before_response = list()

    def after_request_handle(self, func):
        """
        a decorator receive a request object and return a request  after get a request object
        @monk.hook.after_request_handle like this 
        :param func: 
        :return: 
        """
        self.after_request.append(func)
        return func

    def bofore_response_handle(self, func):
        """
        a decorator receive a response object and return a response before send a response object
        :param func: 
        :return: 
        """
        self.before_response.append(func)
        return func

    def clean(self):
        self.before_response.clear()
        self.after_request.clear()

