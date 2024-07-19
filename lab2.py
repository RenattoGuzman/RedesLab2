import numpy as np

def hamming_code(data, n, m):
    """
    Implementa el código de Hamming para corrección de errores.
    
    :param data: Array de bits de datos (debe tener longitud m)
    :param n: Longitud total del código Hamming (datos + bits de paridad)
    :param m: Número de bits de datos
    :return: Array de bits codificados con Hamming
    """
    if len(data) != m:
        raise ValueError(f"La longitud de los datos debe ser {m}")
    
    # Calcular el número de bits de paridad (k) en este caso es 3
    k = n - m
    
    # Crear el array de código Hamming
    code = np.zeros(n, dtype=int)
    
    # Colocar los bits de datos en las posiciones correctas
    j = 0
    for i in range(n):
        if (i + 1) & (i) != 0:  # Si i+1 no es potencia de 2
            code[i] = data[j]
            j += 1
    
    # Calcular los bits de paridad
    for i in range(k):
        parity_pos = 2**i - 1
        parity = 0
        for j in range(parity_pos, n, 2**(i+1)):
            parity ^= np.sum(code[j:min(j+2**i, n)])
        code[parity_pos] = parity % 2
    
    return code

def decode_hamming(received, n, m):
    """
    Decodifica y corrige (si es posible) el código Hamming recibido.
    
    :param received: Array de bits recibidos (longitud n)
    :param n: Longitud total del código Hamming
    :param m: Número de bits de datos originales
    :return: Array de bits de datos corregidos (longitud m)
    """
    if len(received) != n:
        raise ValueError(f"La longitud del código recibido debe ser {n}")
    
    # Calcular el número de bits de paridad (k)
    k = n - m
    
    # Calcular el síndrome
    syndrome = np.zeros(k, dtype=int)
    for i in range(k):
        parity_pos = 2**i - 1
        parity = 0
        for j in range(parity_pos, n, 2**(i+1)):
            parity ^= np.sum(received[j:min(j+2**i, n)])
        syndrome[i] = parity % 2
    
    # Convertir el síndrome a un número decimal
    error_pos = sum([syndrome[i] * 2**i for i in range(k)])
    
    # Corregir el error si existe
    if error_pos != 0:
        print(f"Error en la posición: {error_pos}")
        received[error_pos - 1] ^= 1
    
    # Extraer los bits de datos
    data = np.zeros(m, dtype=int)
    j = 0
    for i in range(n):
        if (i + 1) & (i) != 0:  # Si i+1 no es potencia de 2
            data[j] = received[i]
            j += 1
    
    return data


def fletcher_checksum(data):
    """
    Calcula un Fletcher checksum simplificado de 3 bits.
    
    :param data: Lista o array de bits (0s y 1s) para calcular el checksum.
    :return: Checksum de 3 bits como un entero.
    """
    if not all(bit in (0, 1) for bit in data):
        raise ValueError("Los datos deben ser una secuencia de bits (0s y 1s)")
    
    c0 = c1 = 0
    for bit in data:
        c0 = (c0 + bit) % 4  # Usamos módulo 4 (2^2) para mantener 2 bits
        c1 = (c1 + c0) % 2   # Usamos módulo 2 para el tercer bit
    
    return  f"{c0:02b}{c1:01b}"  # Combinamos c0 (2 bits) y c1 (1 bit) en un checksum de 3 bits

def exists_error(checksum1, checksum2):
    """
    Compara dos checksums y determina si hay un error.
    
    :param checksum1: Checksum original (3 bits)
    :param checksum2: Checksum recibido (3 bits)
    :return: True si hay un error, False en caso contrario
    """
    return checksum1 != checksum2

# Ejemplo de uso
if __name__ == "__main__":
    # Ejemplo con (7,4) Hamming code
    data = np.array([1, 0, 0, 1])
    n, m = 7, 4
    
    encoded = hamming_code(data, n, m)
    print("Datos originales:", data)
    print("Código Hamming:", encoded)
    
    checksum = fletcher_checksum(encoded)
    print("Checksum:", checksum)

    print(f"Hay error: {exists_error(checksum, checksum)}")
    # Simular un error en la transmisión
    received = encoded.copy()
    received[2] ^= 1  # Invertir el tercer bit
    print("Código recibido (con error):", received)
    
    checksum1 = fletcher_checksum(received)
    print("\nChecksum:", checksum1)
    print(f"Hay error: {exists_error(checksum, checksum1)}")


    decoded = decode_hamming(received, n, m)
    print("Datos decodificados y corregidos:", decoded)