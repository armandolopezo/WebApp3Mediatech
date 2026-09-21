from flask import Flask, request, jsonify
from datetime import datetime

app = Flask(__name__)

def get_client_ip(req):
    # Lee la cabecera X-Forwarded-For inyectada por el balanceador de Azure
    x_forwarded_for = req.headers.get('X-Forwarded-For')
    
    if x_forwarded_for:
        # I will print variable  "x_forwarded_for"temporary for curiosity
        print(f"x_forwarded_for: {x_forwarded_for}")
        # La primera IP es la del cliente original
        client_ip = x_forwarded_for.split(',')[0].strip()
    else:
        # Respaldo para peticiones locales directas
        client_ip = req.remote_addr
        
    return client_ip

@app.route("/")
def index():
    # 1. Obtener datos de la visita
    user_ip = get_client_ip(request)
    timestamp = datetime.utcnow().isoformat()
    user_agent = request.headers.get('User-Agent', 'Unknown')

    # 2. Estructurar evento para Azure Table Storage
    event_data = {
        "PartitionKey": datetime.utcnow().strftime("%Y-%m"),
        "RowKey": f"{int(datetime.utcnow().timestamp())}",
        "ClientIP": user_ip,
        "Timestamp": timestamp,
        "UserAgent": user_agent
    }

    # (Opcional) Imprimir en consola de App Service (Application Logs)
    print(f"VISITA REGISTRADA: {event_data}")

    # 3. Retornar la página HTML con el mensaje y la redirección
    return f"""
    <html>
        <body>
            <h1>Welcome! My First Python WEB app, greetings ARMANDO LOPEZ (February 03, 2026) - WAIT SOME SECONDS BEFORE REDIRECTING</h1>
            <p><strong>Your IP:</strong> {user_ip}</p>
            <meta http-equiv="refresh" content="10;url=http://mediatech.com.ec/" />
        </body>
    </html>
    """

# Endpoint secundario para inspeccionar el evento estructurado vía JSON (Opcional)
@app.route("/api/log")
def log_api():
    user_ip = get_client_ip(request)
    return jsonify({
        "status": "success",
        "ClientIP": user_ip,
        "Timestamp": datetime.utcnow().isoformat()
    })

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=80)

