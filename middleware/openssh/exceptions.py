class OpensshException(Exception):
    '''General exception type for openssh failures.'''
    pass


class ScpException(OpensshException):
    '''Scp exception type for openssh failures.'''
    pass

class SshException(OpensshException):
    '''Ssh exception type for openssh failures.'''
    pass
