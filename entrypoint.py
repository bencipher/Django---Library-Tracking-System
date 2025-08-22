import os
import sys
import debugpy


def initialize_debugger(port):
    debugpy.listen(("0.0.0.0", port))
    print(f'VS Code debugger can now be attached on port {port}, press F5 to attach')
    print('Waiting for debugger to attach...')
    # debugpy.wait_for_client()
    print('Debugger attached successfully!')
    # Add a small delay to ensure debugger is fully attached
    import time

    time.sleep(2)


if __name__ == '__main__':
    service_type = sys.argv[1]
    if service_type == 'web':
        print('Running migrations...')
        os.system('python manage.py migrate')
        print('Migrations complete!')
        initialize_debugger(5678)
        os.system('python manage.py runserver 0.0.0.0:8000')
    elif service_type == 'celery':
        initialize_debugger(5679)
        os.system('celery -A library_system worker --beat -l info -E --pool=solo')
    elif service_type == 'flower':
        os.system('celery -A library_system flower --basic_auth=admin:password123')
