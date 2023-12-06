import java.util.Scanner;
class Solution{
	public static void main(String[] args){
		Scanner input = new Scanner(System.in);
		int testCases;
		int num;
		testCases = input.nextInt();
		for (int i = 0; i < testCases;i++){
			num = input.nextInt();
			long res = 1;
			for (int j = 1;j <= num;j++ ){
				res =res * j;
			}
			System.out.println(res);
		}
	}
}