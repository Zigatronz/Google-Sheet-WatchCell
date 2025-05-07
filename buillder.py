
import os, shutil
import PyInstaller.__main__
from time import sleep

main_script = 'main.py'
build_program = os.path.splitext(main_script)[0] + '.exe'

args = [
    '--onefile',
    '--noconsole',
    main_script
]

PyInstaller.__main__.run(args)

try:
    shutil.rmtree('build')
    if os.path.exists(build_program):
        os.remove(build_program)
    os.rename(os.path.join('dist', build_program), build_program)
    shutil.rmtree('dist')
    os.remove(os.path.splitext(main_script)[0] + '.spec')
except:
    print('\nSomething is off while moving exe. You can do it manually.')

print('\n\nBuild completed.')
sleep(3)
