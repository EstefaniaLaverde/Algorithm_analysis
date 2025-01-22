import java.io.BufferedReader;
import java.io.FileReader;
import java.util.ArrayList;

public class ExampleReadTextFile {

	public static void main(String[] args)  throws Exception {
		String filename = args[0];
		ArrayList<Double> numbers = new ArrayList<>();
		
		try (FileReader reader = new FileReader(filename);
			 BufferedReader in = new BufferedReader(reader)) {
			String line = in.readLine();
			while (line != null) {
				numbers.add(Double.parseDouble(line));
				line = in.readLine();
			}
		}
		double sum = 0;
		for(double number:numbers) sum+=number;
		System.out.println("Sum: "+sum);
	}

}
