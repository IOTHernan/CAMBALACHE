#!/bin/bash

# === che_smtp_firmas.sh ===
# Script para generar firmas DKIM, SPF y DMARC para un servidor SMTP
# Compatible con Postfix + OpenDKIM
# Uso: ejecutar en el servidor donde está alojado el dominio

# === CONFIGURACIÓN INICIAL ===
DOMAIN="tudominio.com"
SELECTOR="chekey"
DKIM_DIR="/etc/opendkim/keys/$DOMAIN"

# === Crear directorios y claves ===
echo "[+] Generando claves DKIM para el dominio: $DOMAIN"
mkdir -p "$DKIM_DIR"
cd "$DKIM_DIR"

opendkim-genkey -s "$SELECTOR" -d "$DOMAIN"
chown opendkim:opendkim $SELECTOR.private
chmod 600 $SELECTOR.private

# === Mostrar TXT para agregar al DNS ===
echo "[+] Clave pública generada. Agregue el siguiente registro TXT a su DNS:"
echo ""
echo "Nombre del registro: $SELECTOR._domainkey.$DOMAIN"
echo "Contenido TXT:"
cat "$SELECTOR.txt"
echo ""

# === SPF ===
echo "[+] Ejemplo de entrada SPF a agregar en su DNS:"
echo "@  IN TXT  \"v=spf1 mx a ip4:TU.IP.VALIDA -all\""
echo ""

# === DMARC ===
echo "[+] Entrada DMARC sugerida para el DNS:"
echo "_dmarc.$DOMAIN IN TXT \"v=DMARC1; p=quarantine; rua=mailto:admin@$DOMAIN\""
echo ""

# === Instrucciones adicionales ===
echo "[!] Asegúrese de agregar estas líneas en /etc/opendkim.conf:"
echo ""
echo "Domain                  $DOMAIN"
echo "KeyFile                 $DKIM_DIR/$SELECTOR.private"
echo "Selector                $SELECTOR"
echo "Socket                  inet:12301@localhost"
echo ""
echo "[!] Y configure Postfix (main.cf) con:"
echo "    milter_default_action = accept"
echo "    milter_protocol = 6"
echo "    smtpd_milters = inet:localhost:12301"
echo "    non_smtpd_milters = inet:localhost:12301"
echo ""
echo "[+] Reinicie los servicios:"
echo "    systemctl restart opendkim"
echo "    systemctl restart postfix"
echo ""
echo "[OK] Listo. El servidor ahora firmará los correos salientes con DKIM."
