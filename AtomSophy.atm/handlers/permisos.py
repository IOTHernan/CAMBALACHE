class User:
    def __init__(self, username, permissions):
        self.username = username
        self.permissions = permissions

def has_permission(user, permission):
    """
    Verifica si un usuario tiene un permiso específico.

    Parámetros:
    - user: Instancia de la clase User.
    - permission: Permiso a verificar.

    Retorna:
    - True si el usuario tiene el permiso, False en caso contrario.
    """
    return permission in user.permissions

# Ejemplo de uso:
#user = User('juanp', ['read', 'write', 'delete'])
#print(has_permission(user, 'write'))  # Debería retornar True
#print(has_permission(user, 'execute'))  # Debería retornar False


def assign_permission(user, permission):
    """
    Asigna un permiso a un usuario.

    Parámetros:
    - user: Instancia de la clase User.
    - permission: Permiso a asignar.

    Retorna:
    - None.
    """
    if permission not in user.permissions:
        user.permissions.append(permission)

# Ejemplo de uso:
#assign_permission(user, 'execute')
#print(user.permissions)  # ['read', 'write', 'delete', 'execute']


def revoke_permission(user, permission):
    """
    Revoca un permiso de un usuario.

    Parámetros:
    - user: Instancia de la clase User.
    - permission: Permiso a revocar.

    Retorna:
    - None.
    """
    if permission in user.permissions:
        user.permissions.remove(permission)

# Ejemplo de uso:
#revoke_permission(user, 'delete')
#print(user.permissions)  # ['read', 'write', 'execute']


def can_access_resource(user, resource):
    """
    Verifica si un usuario puede acceder a un recurso basado en sus permisos.

    Parámetros:
    - user: Instancia de la clase User.
    - resource: Recurso al que se quiere acceder.

    Retorna:
    - True si el usuario tiene permiso para acceder, False en caso contrario.
    """
    resource_permissions = {
        'documento_privado': ['read', 'write'],
        'documento_publico': ['read'],
        'documento_confidencial': ['read', 'write', 'delete']
    }

    required_permissions = resource_permissions.get(resource, [])
    return all(has_permission(user, perm) for perm in required_permissions)

# Ejemplo de uso:
#print(can_access_resource(user, 'documento_privado'))  # Debería retornar True
#print(can_access_resource(user, 'documento_confidencial'))  # Debería retornar False

# *******************************************************************+

def restringir_permisos(archivo: str):
    """
    Restringe los permisos del archivo, denegando acceso al sistema.
    """
    cmd = f"""
    PowerShell -Command "
    icacls '{archivo}' /deny SYSTEM:(F)"
    """
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    if result.returncode == 0:
        print(f"[*] Permisos restringidos para {archivo}.")
    else:
        print(f"[Error] No se pudo restringir permisos: {result.stderr}")


def restaurar_permisos(archivo: str):
    """
    Restaura permisos originales, permitiendo acceso al sistema.
    """
    cmd = f"""
    PowerShell -Command "
    icacls '{archivo}' /remove:d SYSTEM"
    """
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    if result.returncode == 0:
        print(f"[*] Permisos restaurados para {archivo}.")
    else:
        print(f"[Error] No se pudo restaurar permisos: {result.stderr}")


def proteger_archivo(ruta_original: str, copia_segura: str):
    """
    Monitorea un archivo y lo restaura si es eliminado.
    """
    while True:
        if not os.path.exists(ruta_original):
            print(f"[!] El archivo {ruta_original} fue eliminado. Restaurando...")
            try:
                shutil.copy(copia_segura, ruta_original)
                print(f"[*] Archivo restaurado desde {copia_segura}.")
            except Exception as e:
                print(f"[Error] No se pudo restaurar el archivo: {e}")
        time.sleep(5)  # Revisar cada 5 segundos


def registrar_eventos(archivo: str, eventos_a_buscar=("4663", "4656")):
    """
    Busca eventos relacionados con la eliminación del archivo en el Visor de Eventos.
    """
    server = "localhost"
    log_type = "Security"
    events = []

    # Abre el registro del Visor de Eventos
    handle = win32evtlog.OpenEventLog(server, log_type)
    flags = win32evtlog.EVENTLOG_BACKWARDS_READ | win32evtlog.EVENTLOG_SEQUENTIAL_READ

    # Lee los eventos
    while True:
        records = win32evtlog.ReadEventLog(handle, flags, 0)
        if not records:
            break
        for record in records:
            if any(event_id in str(record.EventID) for event_id in eventos_a_buscar):
                if archivo in record.StringInserts:
                    events.append(
                        {
                            "EventoID": record.EventID,
                            "Fuente": record.SourceName,
                            "Usuario": record.UserSid,
                            "Mensaje": record.StringInserts,
                        }
                    )

    win32evtlog.CloseEventLog(handle)
    return events


# mi_libreria/ssh.py


def ssh_execute_command(host, username, password, command):
    """
    Función para conectarse a un servidor SSH y ejecutar un comando.

    Parámetros:
    - host: Dirección IP o nombre del servidor.
    - username: Nombre de usuario para SSH.
    - password: Contraseña del usuario SSH.
    - command: Comando a ejecutar en el servidor remoto.

    Retorna:
    - stdout: La salida estándar del comando.
    - stderr: La salida de error del comando, si existe.
    """
    ssh = paramiko.SSHClient()
    ssh.load_system_host_keys()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    try:
        ssh.connect(host, username=username, password=password)
        stdin, stdout, stderr = ssh.exec_command(command)
        output = stdout.read().decode()
        error = stderr.read().decode()
        return output, error
    finally:
        ssh.close()


# Ejemplo de uso:
#output, error = ssh_execute_command(
#    host='ip-del-servidor',
#    username='usuario',
#    password='tu-contraseña',
#    command='ls -l'
#)
#if error:
#    print("Error:", error)
#else:
#    print("Salida:", output)
    
    
def ssh_transfer_file(host, username, password, local_file, remote_file):
    """
    Función para transferir archivos a través de SSH (SCP).

    Parámetros:
    - host: Dirección del servidor SSH.
    - username: Nombre de usuario para SSH.
    - password: Contraseña del usuario SSH.
    - local_file: Ruta del archivo local.
    - remote_file: Ruta del archivo remoto donde se copiará.

    Retorna:
    - None.
    """
    ssh = paramiko.SSHClient()
    ssh.load_system_host_keys()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    try:
        ssh.connect(host, username=username, password=password)
        sftp = ssh.open_sftp()
        sftp.put(local_file, remote_file)
        sftp.close()
    finally:
        ssh.close()

# Ejemplo de uso:
#ssh_transfer_file(
#    host='ip-del-servidor',
#    username='usuario',
#    password='tu-contraseña',
#    local_file='/ruta/al/archivo-local.txt',
#    remote_file='/ruta/remota/al/archivo.txt'
#)


# mi_libreria/oauth.py *****************************************************************************

from authlib.integrations.requests_client import OAuth2Session

def oauth2_login(client_id, client_secret, redirect_uri, auth_endpoint, token_endpoint):
    """
    Función para manejar el flujo de OAuth2.

    Parámetros:
    - client_id: ID de cliente de OAuth2.
    - client_secret: Secreto de cliente de OAuth2.
    - redirect_uri: URI de redirección tras autenticación.
    - auth_endpoint: URL del proveedor de OAuth2 para la autenticación.
    - token_endpoint: URL del proveedor para obtener el token.

    Retorna:
    - access_token: El token de acceso obtenido.
    """
    session = OAuth2Session(client_id, client_secret, redirect_uri=redirect_uri)
    authorization_url, state = session.create_authorization_url(auth_endpoint)

    print("Visita esta URL para iniciar sesión:", authorization_url)

    code = input("Ingresa el código de la URL: ")
    token = session.fetch_token(token_endpoint, code=code)

    return token['access_token']


# Ejemplo de uso:
# token = oauth2_login(
#   client_id='tu-client-id',
#   client_secret='tu-client-secret',
#   redirect_uri='https://tu-redirect-uri.com',
#   auth_endpoint='https://login.microsoftonline.com/common/oauth2/v2.0/authorize',
#   token_endpoint='https://login.microsoftonline.com/common/oauth2/v2.0/token'
# )
# print("Access Token:", token)


def verify_token(session, protected_url, access_token):
    """
    Función para verificar si un token de acceso OAuth2 sigue siendo válido.

    Parámetros:
    - session: Instancia de OAuth2Session.
    - protected_url: URL protegida a la que se hace la solicitud.
    - access_token: Token de acceso que se verifica.

    Retorna:
    - response_data: La respuesta de la API si el token es válido.
    """
    headers = {'Authorization': f'Bearer {access_token}'}
    response = session.get(protected_url, headers=headers)

    if response.status_code == 200:
        return response.json()
    else:
        return None
