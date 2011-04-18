class TPasswdFile(object):
    """
    Provides an interface for querying and updating an SRP passwd file using
    the srptool/GnuTLS tpasswd format.
    """
    
    def __init__(self, path):
        self.path = path

    def get(self, username):
        """
        Returns the last entry in the tpasswd file for `username`.
        """
        if not username:
            raise KeyError("username must be non-empty")
        if ':' in username:
            raise KeyError("username must not contain colon (':') delimiter")
        info = None
        with open(self.path) as f:
            for line in f:
                if line.startswith(username + ':'):
                    info = self.__parse_line(line)
        return info

    def put(self, username, verifier, salt, group_index):
        with open(self.path, 'a') as f:
            f.write(':'.join((username, verifier, salt, str(group_index))))
            f.write("\n")
    
    def __parse_line(self, line):
        parts = line.split(':')
        return {
            'username': parts[0],
            'verifier': parts[1],
            'salt': parts[2],
            'group_index': int(parts[3]),
        }

    
