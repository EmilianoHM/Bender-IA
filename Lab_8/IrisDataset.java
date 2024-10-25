import java.io.BufferedReader;
import java.io.FileReader;
import java.io.IOException;
import java.util.ArrayList;

public class IrisDataset {
    public static void main(String[] args) {
        String file = "bezdekIris.data";  // Definimos la ruta del archivo que vamos a leer.
        ArrayList<String[]> dataset = new ArrayList<>();  // Usamos un ArrayList para almacenar cada fila como un arreglo de cadenas.
        String line;  // Variable que almacenará cada línea leída del archivo.
        
        try (BufferedReader br = new BufferedReader(new FileReader(file))) {
            // El bloque 'try-with-resources' abre el archivo y se asegura de cerrarlo automáticamente.
            while ((line = br.readLine()) != null) {
                // Mientras existan líneas por leer, las procesamos.
                
                // Dividimos cada línea en partes usando la coma como separador.
                String[] data = line.split(",");
                
                // Agregamos el arreglo resultante (una fila del dataset) al ArrayList.
                dataset.add(data);
            }
        } catch (IOException e) {
            // Si ocurre un error durante la lectura del archivo, lo manejamos aquí.
            e.printStackTrace();
        }

        // Imprimimos los títulos de las columnas con un formato tabulado.
        System.out.println(String.format("%-15s %-15s %-15s %-15s %-20s", 
                "sepal_length", "sepal_width", "petal_length", "petal_width", "class"));
        System.out.println("---------------------------------------------------------------------------");

        // Imprimimos las primeras 5 filas del dataset con un formato tabulado.
        for (int i = 0; i < 5; i++) {
            System.out.println(String.format("%-15s %-15s %-15s %-15s %-20s", 
                dataset.get(i)[0], dataset.get(i)[1], dataset.get(i)[2], dataset.get(i)[3], dataset.get(i)[4]));
        }
    }
}
