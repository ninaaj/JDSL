/*
	Course: CSCI 111-4 
	Student Name: Christina Trotter 
	Student ID: 10373033 
	Program 5 
	Due Date: 5/5/18 
	Honor Code: In keeping with the Honor Code of UM, I have neither given nor received assistance from anyone other than the instructor. 
	Program Description: This program determines whether an input year is a leap year. 
*/
import java.util.Scanner;

public class LeapYear {

	public static void main (String[] args){

		//variables and Scanner object 

		String again;

		int year;

		Scanner scan;

		boolean leap;

		//instantiate Scanner object and get user input 

		scan = new Scanner(System.in);

		System.out.print("Do you want to enter a year? yes/no: ");

		again = scan.nextLine();

		while (again.equals("yes") ) {

		System.out.print("Enter a 4-digit year: ");

		year = scan.nextInt();

		//call user-defined method 

		leap = isLeap(year);

		if (leap ) {

		System.out.printf("%d is a leap year.\n ",year);

		}

		else {

		System.out.printf("%d is not a leap year.\n ",year);

		}

		scan.nextLine();

		System.out.print("\nDo you want to enter a year? yes/no: ");

		again = scan.nextLine();

		}

	}

		//user-defined isLeap method 

	public static boolean isLeap (int year){

		if ((year % 4) == 0 && (year % 100) != 0 || (year % 100) == 0 && (year % 400) == 0 ) {

		return true ;

		}

		else {

		return false ;

		}

	}

}

