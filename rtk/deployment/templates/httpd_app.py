
config = '''
<IfDefine !IS_DJANGOSTACK_LOADED>
    Define IS_DJANGOSTACK_LOADED
    WSGIDaemonProcess wsgi-djangostack processes=2 threads=15 display-name=%{GROUP}
</IfDefine>

    Alias {app}/static "{path}/{app}/RTKWebApp/static"
    WSGIScriptAlias /{app} "{path}/{app}/RTKWebApp/wsgi.py"
    
    <Directory "{path}/{app}/RTKWebApp/">
        WSGIProcessGroup wsgi-djangostack
        WSGIApplicationGroup %{GLOBAL}
    <IfVersion < 2.3 >
        Order allow,deny
        Allow from all
    </IfVersion>
    <IfVersion >= 2.3>
        Require all granted
    </IfVersion>
 </Directory>
'''