class SshUtil:
        
    def __init__(self, hostname, username, password):
        #### start patching crypto ####
        # Monkey patches cryptography's backend detection.
        from cryptography.hazmat import backends

        try:
            from cryptography.hazmat.backends.commoncrypto.backend import backend as be_cc
        except ImportError:
            be_cc = None

        try:
            from cryptography.hazmat.backends.openssl.backend import backend as be_ossl
        except ImportError:
            be_ossl = None

        backends._available_backends_list = [ be for be in (be_cc, be_ossl) if be is not None ]
        #### end patching crypto ####
        
        import paramiko
        s = paramiko.SSHClient()
        s.load_system_host_keys()
        s.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        self.client = s
        self.hostname = hostname
        self.username = username
        self.password = password
    
    def cmd(self, command): 
        self.client.connect(self.hostname, 22, self.username, self.password)
        # kinit will fail on Basic clusters, but that can be ignored
        self.client.exec_command('kinit -k -t {0}.keytab {0}@IBM.COM'.format(self.username))
        (stdin, stdout, stderr) = self.client.exec_command(command)
        for line in stdout.readlines():
            print line.rstrip()
        for line in stderr.readlines():
            print line.rstrip()
        s.close()
        
    def put(self, filenames):
        from scp import SCPClient
        self.client.connect(self.hostname, 22, self.username, self.password)
        # kinit will fail on Basic clusters, but that can be ignored
        self.client.exec_command('kinit -k -t {0}.keytab {0}@IBM.COM'.format(self.username))
        with SCPClient(self.client.get_transport()) as scp:
            scp.put(filenames)
        scp.close()

    def get(self, filenames):
        from scp import SCPClient
        self.client.connect(self.hostname, 22, self.username, self.password)
        # kinit will fail on Basic clusters, but that can be ignored
        self.client.exec_command('kinit -k -t {0}.keytab {0}@IBM.COM'.format(self.username))
        with SCPClient(self.client.get_transport()) as scp:
            scp.get(filenames)
