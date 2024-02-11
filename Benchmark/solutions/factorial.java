import java.util.Scanner;

public class factorial{
    static int fact(int n){
        if (n <= 1){
            return 1;
        }
        return n * fact(n-1);
    }
    
    public static void main(String[] args){
    Scanner input = new Scanner(System.in);
    int testCases = input.nextInt();
    input.nextLine();
    for(int i =0;i < testCases;i++){
        int result,num;
        num = input.nextInt();
        result = fact(num);
        System.out.println(result);
    }
    }
}