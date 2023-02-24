from datetime import datetime

ahora = datetime.now()

# Formato de hora por defecto
print("Hora actual (formato por defecto):", ahora)

# Cambio de formato de hora
hora_formateada = ahora.strftime("%H:%M:%S")
print("Hora actual (formato personalizado):", hora_formateada)
