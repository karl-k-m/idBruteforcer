import java.io.FileWriter;
import java.io.IOException;
import java.util.ArrayList;
import java.util.List;
import java.util.Scanner;

public class idBruteforcer {
    static boolean checkControlNumber(long n) {
        String temp = Long.toString(n);
        int[] nArray = new int[temp.length()];
        for (int i = 0; i < temp.length(); i++) {
            nArray[i] = temp.charAt(i) - '0';
        }

        int total = 0;

        for (int i = 0; i < 9; i++) {
            total += nArray[i] * (i + 1);
        }
        total += nArray[9];

        total = (int) Math.floor(total % 11);

        if (total == 10) {
            total = 0;

            for (int i = 0; i < 7; i++) {
                total += nArray[i] * (i + 3);
            }
            total += nArray[7];
            total += nArray[8] * 2;
            total += nArray[9] * 3;

            total = (int) Math.floor(total % 11);
        }

        return total == nArray[10];
    }

    public static int getFirstNr(boolean isMale, String DoB) {
        int year = Integer.parseInt(DoB.substring(0, 2));
        if (isMale) {
            if (year > 23) {
                return 3;
            }
            return 5;
        }
        if (year > 23) {
            return 4;
        }
        return 6;
    }

    public static List<Long> bruteforceIds(boolean isMale, String DoB) {
        List<Long> checked = new ArrayList<>();
        for (int i = 1; i < 10000; i++) {
            long id = Long.parseLong(getFirstNr(isMale, DoB) + DoB + String.format("%04d", i));
            if (checkControlNumber(id)) {
                checked.add(id);
            }
        }
        return checked;
    }

    public static void main(String[] args) {
        //String dob = "030207";
        //List<Long> list = bruteforceIds(true, dob);
        //for (Long i : list) {
        //    System.out.println(i);
        //}
        //System.out.println("many:" + list.size());

        Scanner scanner = new Scanner(System.in);

        System.out.println("Enter date of birth (YYMMDD):");
        String dob = scanner.nextLine();

        System.out.println("Is target male or female? (m/f)");
        String gender = scanner.nextLine();

        List<Long> list = new ArrayList<>();
        switch (gender) {
            case "m" -> list = bruteforceIds(true, dob);
            case "f" -> list = bruteforceIds(false, dob);
        }

        System.out.println("many:" + list.size());

        try {
            FileWriter writer = new FileWriter(gender + "_" + dob + ".txt");
            for (Long i : list) {
                writer.write(i + "\n");
            }
            writer.close();
        } catch (IOException e) {
            e.printStackTrace();
        }
    }
}