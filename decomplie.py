import fnmatch
import os
import glob
import Queue
import subprocess
import threading

package = 'DemoForchenganyanshi_2.0'
javapath = 'apk/' + package + '/java'
if not os.path.exists(javapath):
    os.makedirs(javapath)
q = Queue.Queue()

for root, dirnames, filenames in os.walk('DemoForchenganyanshi_2.0'):
    for filename in fnmatch.filter(filenames, '*.class'):
        if '$' not in filename:
            q.put(os.path.join(root, filename))


print q

# classes = glob.glob(package + '/**/*.class')
# for file in classes:
#     q.put(file)


def decomplie_class():
    while True:
        file = q.get()
        relpath = os.path.relpath(file, 'DemoForchenganyanshi_2.0/')
        if '$' in os.path.basename(file):
            pass
        else:
            tarpath = 'cfr-decompile-demo-apk/java/' + os.path.dirname(relpath)
            if os.path.exists(tarpath + '/' + os.path.splitext(os.path.basename(file))[0] + '.java'):
                print(tarpath + '/' + os.path.basename(file) + 'exists')
            else:
                if not os.path.exists(tarpath):
                    try:
                        os.makedirs(tarpath)
                    except:
                        pass

                nested_class = []
                for file2 in glob.glob(os.path.dirname(file) + '/*.class'):
                    if os.path.basename(file2).startswith(os.path.basename(file)[0] + '$'):
                        nested_class.append(file2)
                commend = ('java -jar cfr.jar'.split(' '))
                commend.append(file)
                commend.append('--outputdir')
                commend.append(tarpath)
                subprocess.call(commend)
                print file
        q.task_done()


for i in range(8):
    t = threading.Thread(target=decomplie_class)
    t.daemon = True  # thread dies when main thread (only non-daemon thread) exits.
    t.start()

q.join()
