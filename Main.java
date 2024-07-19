import java.util.Arrays;

public class Main {

    public static int[] hammingCode(int[] data, int n, int m) {
        if (data.length != m) {
            throw new IllegalArgumentException("La longitud de los datos debe ser " + m);
        }

        int k = n - m;
        int[] code = new int[n];

        // Colocar los bits de datos en las posiciones correctas
        int j = 0;
        for (int i = 0; i < n; i++) {
            if ((i + 1 & i) != 0) {  // Si i+1 no es potencia de 2
                code[i] = data[j++];
            }
        }

        // Calcular los bits de paridad
        for (int i = 0; i < k; i++) {
            int parityPos = (1 << i) - 1;
            int parity = 0;
            for (int pos = parityPos; pos < n; pos += (1 << (i + 1))) {
                for (int bit = 0; bit < (1 << i) && pos + bit < n; bit++) {
                    parity ^= code[pos + bit];
                }
            }
            code[parityPos] = parity;
        }

        return code;
    }

    public static int[] decodeHamming(int[] received, int n, int m) {
        if (received.length != n) {
            throw new IllegalArgumentException("La longitud del código recibido debe ser " + n);
        }

        int k = n - m;
        int[] syndrome = new int[k];

        // Calcular el síndrome
        for (int i = 0; i < k; i++) {
            int parityPos = (1 << i) - 1;
            int parity = 0;
            for (int pos = parityPos; pos < n; pos += (1 << (i + 1))) {
                for (int bit = 0; bit < (1 << i) && pos + bit < n; bit++) {
                    parity ^= received[pos + bit];
                }
            }
            syndrome[i] = parity;
        }

        // Convertir el síndrome a un número decimal
        int errorPos = 0;
        for (int i = 0; i < k; i++) {
            errorPos += syndrome[i] * (1 << i);
        }

        // Corregir el error si existe
        if (errorPos != 0) {
            System.out.println("Error en la posición: " + errorPos);
            received[errorPos - 1] ^= 1;
        }

        // Extraer los bits de datos
        int[] data = new int[m];
        int j = 0;
        for (int i = 0; i < n; i++) {
            if ((i + 1 & i) != 0) {  // Si i+1 no es potencia de 2
                data[j++] = received[i];
            }
        }

        return data;
    }

    public static String fletcherChecksum(int[] data) {
        for (int bit : data) {
            if (bit != 0 && bit != 1) {
                throw new IllegalArgumentException("Los datos deben ser una secuencia de bits (0s y 1s)");
            }
        }

        int c0 = 0, c1 = 0;
        for (int bit : data) {
            c0 = (c0 + bit) % 4;  // Usamos módulo 4 (2^2) para mantener 2 bits
            c1 = (c1 + c0) % 2;   // Usamos módulo 2 para el tercer bit
        }

        return String.format("%d%d%d", c0 / 2, c0 % 2, c1);  // Combinamos c0 (2 bits) y c1 (1 bit) en un checksum de 3 bits
    }

    public static boolean existsError(String checksum1, String checksum2) {
        return !checksum1.equals(checksum2);
    }

    public static void main(String[] args) {
        // Ejemplo con (7,4) Hamming code
        int[] data = {1, 0, 0, 1};
        int n = 7, m = 4;

        int[] encoded = hammingCode(data, n, m);
        System.out.println("Datos originales: " + Arrays.toString(data));
        System.out.println("Código Hamming: " + Arrays.toString(encoded));

        String checksum = fletcherChecksum(encoded);
        System.out.println("Checksum: " + checksum);

        System.out.println("Hay error: " + existsError(checksum, checksum));

        // Simular un error en la transmisión
        int[] received = Arrays.copyOf(encoded, encoded.length);
        received[2] ^= 1;  // Invertir el tercer bit
        System.out.println("Código recibido (con error): " + Arrays.toString(received));

        String checksum1 = fletcherChecksum(received);
        System.out.println("\nChecksum: " + checksum1);
        System.out.println("Hay error: " + existsError(checksum, checksum1));

        int[] decoded = decodeHamming(received, n, m);
        System.out.println("Datos decodificados y corregidos: " + Arrays.toString(decoded));
    }
}