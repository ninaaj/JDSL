		//this is a multiclass test program 

public class MultiClasses {

	public static void main (String[] args){

		System.out.print("I'm the public class! ");

		SubClass sc;

		sc = new SubClass();

	}

}

class SubClass {

	public static void main (String[] args){

		System.out.print("I'm the regular class! ");

	}

}

