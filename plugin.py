import sublime, sublime_plugin
from subprocess import Popen, PIPE
from sys import getfilesystemencoding
from time import time,sleep
from os import path, chdir, getcwd

class wpclievalselectionCommand(sublime_plugin.TextCommand):
    def get_settings(self):
        settings = {}

        user = self.view.settings().get('wp_cli_eval_selection')

        if user:
            settings['cli_path'] = user['cli_path'] if 'cli_paths' in user else None
        else:
            settings = {'cli_path': None}

        return settings

    def run(self, edit):
        window = self.view.window()
        status = ''

        settings = self.get_settings()
        working_dir = None

        for region in self.view.sel():
            if region.empty():
                continue

            code = self.view.substr(region)

            # shell script
            script = 'pwd; wp eval "$(cat <<EOF' + '\n' + code + '\n' + 'EOF)"'

            if settings['cli_path']:
                script += ' --path=' + settings['cli_path']
            elif not working_dir:
                working_dir = getcwd()
                chdir(path.dirname( self.view.file_name() ))

            # sublime.status_message('Evaluating code `' + code[15:] + '`' + ( '...' if len(code) > 15 else '' ))

            # record begin time
            start = time()

            # execute code on subprocess
            cli = Popen(script, shell=True, stdout=PIPE, stderr=PIPE).communicate()
            
            # counting the time spent in seconds
            ms_spent = time() - start

            # shell stdout
            stdout = cli[0].decode(getfilesystemencoding())
            
            # shell stderr
            stderr = cli[1].decode(getfilesystemencoding())

            status += '=======================\n\n'
            status += '> Evaluating code\n\n`' + code + '`\n\n'
            
            if stderr:
                status += '> Evaluation has ended with an error\n\n' + stderr + '\n\n'
                # sublime.status_message('Error evaluating code')
            else:
                status += '> Response\n\n' + stdout + '\n\n'
                status += '> Evaluated in\n\n' + str( round( ms_spent, 2 ) ) + ' s\n\n'
                # sublime.status_message('Success!')

        if status:
            # sublime.status_message('Writing full eval log')
            f = window.new_file()
            f.insert( edit, 0, '\n' + status )

            if working_dir:
                # popd
                chdir( working_dir )
