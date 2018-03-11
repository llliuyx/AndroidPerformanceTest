import subprocess
import os

class Adb(object):

    @staticmethod
    def exec_shell_cmd(device_serial, cmd_base):
        cmd_line = "adb -s %s shell %s" % (device_serial, cmd_base)
        print cmd_line
        return subprocess.Popen(cmd_line, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    # def cmd(self, *args, **kwargs):
    #     '''adb command, add -s serial by default. return the subprocess.Popen object.'''
    #     serial = self.device_serial()
    #     if serial:
    #         if " " in serial:  # TODO how to include special chars on command line
    #             serial = "'%s'" % serial
    #         return self.raw_cmd(*["-s", serial] + list(args))
    #     else:
    #         return self.raw_cmd(*args)
    #
    # def raw_cmd(self, *args):
    #     '''adb command. return the subprocess.Popen object.'''
    #     cmd_line = [self.adb()] + self.adbHostPortOptions + list(args)
    #     if os.name != "nt":
    #         cmd_line = [" ".join(cmd_line)]
    #     return subprocess.Popen(cmd_line, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
