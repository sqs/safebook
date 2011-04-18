class TPasswdFile(object):
    """
    Provides an interface for querying and updating an SRP passwd file using
    the srptool/GnuTLS tpasswd format.
    """
    
    def __init__(self, path):
        self.path = path

    def get(self, username):
        """
        Returns the entry in the tpasswd file for `username`.
        """
        self.__check_username(username)
        with open(self.path) as f:
            for line in f:
                if line.startswith(username + ':'):
                    return self.__parse_line(line)
        return None

    def delete(self, username):
        """
        Deletes a user's entry from the file.
        TODO(sqs): this requires copying and rewriting the whole file. very
        inefficient and dangerous (if concurrent accesses).
        """
        self.__check_username(username)
        lines = []
        with open(self.path, 'r+b') as f:
            for line in f:
                if not line.startswith(username + ':'):
                    lines.append(line)
            f.truncate(0)
            f.seek(0)
            f.write(''.join(lines))
    
    def put(self, username, verifier, salt, group_index):
        self.__check_username(username)
        self.delete(username)
        with open(self.path, 'a') as f:
            f.write(':'.join((username, verifier, salt, str(group_index))))
            f.write("\n")

    def __check_username(self, username):
        if not username:
            raise KeyError("username must be non-empty")
        if ':' in username:
            raise KeyError("username must not contain colon (':') delimiter")
            
    def __parse_line(self, line):
        parts = line.split(':')
        return {
            'username': parts[0],
            'verifier': parts[1],
            'salt': parts[2],
            'group_index': int(parts[3]),
        }

    
