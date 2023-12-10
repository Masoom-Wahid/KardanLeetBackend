
import java.io.File;
import java.io.FileNotFoundException;
import java.io.IOException;
import java.io.InputStream;
import java.io.InputStreamReader;
import java.nio.charset.StandardCharsets;
import java.nio.file.Files;
import java.util.Scanner;

public class execute{
    public static void main(String[] args) {
        try {
            String[] arguments = new String[args.length];
            System.arraycopy(args, 0, arguments, 0, args.length);
            // Specify the path to the Java file you want to execute
            int num_of_test_cases = Integer.parseInt(arguments[0]);
            String className = arguments[1];
            String javaFilePath = arguments[2];
            String questionsPath = arguments[3];
            String questionName = arguments[4];
            long TIMEOUT = 10000;
            // Execute the Java file using the Java compiler
            Process process = Runtime.getRuntime().exec("javac " + javaFilePath);
            int exitCode = process.waitFor();
            if (exitCode == 0) {
                for (int i = 1;i <= num_of_test_cases;i++){    
                Process executionProcess = Runtime.getRuntime().exec("java " + className);
                String inputname = questionsPath+"/"+questionName+"input"+i+".txt";
                String outputname = questionsPath+"/"+questionName+"output"+i+".txt";
                try{
                    // Pass input from input.txt to the executed Java program
                    Thread timeoutThread = new Thread(() -> {
                        try{
                            Thread.sleep(TIMEOUT);
                            executionProcess.destroy();
                            System.exit(2);
                        }catch(InterruptedException e){
                            executionProcess.destroy();
                            System.exit(2);
                        }
                    });
                    timeoutThread.start();
                    File inputFile = new File(inputname);
                    Scanner inputScanner = new Scanner(inputFile);
                    while (inputScanner.hasNextLine()) {
                        String line = inputScanner.nextLine();
                        executionProcess.getOutputStream().write((line + "\n").getBytes(StandardCharsets.UTF_8));
                    }
                    inputScanner.close();
                    executionProcess.getOutputStream().close();
    
                    int executionExitCode = executionProcess.waitFor();
    
    
                    // Capture the output and error streams of the executed Java program
                    String output = readStream(executionProcess.getInputStream());
                    // String error = readStream(executionProcess.getErrorStream());
                    if (executionExitCode == 0) {
                        // Compare the output with the contents of output.txt
                        File outputFile = new File(outputname);
                        String expectedOutput = Files.readString(outputFile.toPath(), StandardCharsets.UTF_8);
                        // System.out.println(output.trim());
                        // System.out.println("***********************************************************");
                        // System.out.println(expectedOutput.trim());
                        if (!output.trim().equals(expectedOutput.trim())) {
                            System.exit(1);
                        }
                    } else {
                        System.exit(1);
                    }
                }catch(Exception e){
                    System.exit(2);
                } 
            }

            System.exit(0);
            // long endTime = System.nanoTime();
            // long executionTime = endTime - startTime;
            // double durationInSeconds = (double) executionTime / 1_000_000_000;
            // System.out.println("Duration in seconds: " + durationInSeconds);
            // System.out.println("--------------------------------------------------------");
            } else {
                System.exit(1);
            }
        } catch (FileNotFoundException e) {
            System.exit(1);
        } catch (IOException | InterruptedException e) {
            System.exit(1);
        }
    }

    private static String readStream(InputStream inputStream) {
        StringBuilder output = new StringBuilder();
        try (Scanner scanner = new Scanner(new InputStreamReader(inputStream, StandardCharsets.UTF_8))) {
            while (scanner.hasNextLine()) {
                String line = scanner.nextLine();
                output.append(line).append("\n");
            }
        }
        return output.toString();
    }
}