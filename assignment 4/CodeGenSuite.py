# 1652579 - Pham Ngoc Thoai
import unittest
from TestUtils import TestCodeGen
from AST import *

class CheckCodeGenSuite(unittest.TestCase):
    def test_simple_put_int(self):
        input = """void main(){
            2;
            putInt(2*(3+(2-(3+2))));
        }"""
        expect = "0"
        self.assertTrue(TestCodeGen.test(input, expect, 500))

    def test_simple_put_int_new_line(self):
        input = """void main(){
            putIntLn(1);
        }"""
        expect = "1\n"
        self.assertTrue(TestCodeGen.test(input, expect, 501))

    def test_simple_put_float(self):
        input = """void main(){
            putFloat(2.1);
        }"""
        expect = "2.1"
        self.assertTrue(TestCodeGen.test(input, expect, 502))

    def test_simple_put_float_new_line(self):
        input = """void main(){
            putFloatLn(100.001);
        }"""
        expect = "100.001\n"
        self.assertTrue(TestCodeGen.test(input, expect, 503))

    def test_simple_put_bool(self):
        input = """void main(){
            putBool(true);
        }"""
        expect = "true"
        self.assertTrue(TestCodeGen.test(input, expect, 504))

    def test_simple_put_string(self):
        input = """void main(){
            putString("string");
        }"""
        expect = "string"
        self.assertTrue(TestCodeGen.test(input, expect, 505))

    def test_simple_put_string_new_line(self):
        input = """void main(){
            putStringLn("string");
        }"""
        expect = "string\n"
        self.assertTrue(TestCodeGen.test(input, expect, 506))

    def test_simple_add_op_int(self):
        input = """void main(){
            putInt(1+1);
        }"""
        expect = "2"
        self.assertTrue(TestCodeGen.test(input, expect, 507))

    def test_big_add_op_int(self):
        input = """void main(){
            putIntLn(12345+12345);
        }"""
        expect = "24690\n"
        self.assertTrue(TestCodeGen.test(input, expect, 508))

    def test_simple_minus_op_int(self):
        input = """void main(){
            putInt(9999-99999);
        }"""
        expect = "-90000"
        self.assertTrue(TestCodeGen.test(input, expect, 509))

    def test_many_add_op_int(self):
        input = """void main(){
            putInt(1+2+3+4+5+99);
        }"""
        expect = "114"
        self.assertTrue(TestCodeGen.test(input, expect, 510))

    def test_many_add_op_float_int(self):
        input = """void main(){
            putFloat(4+5.5+2+1.111);
        }"""
        expect = "12.611"
        self.assertTrue(TestCodeGen.test(input, expect, 511))

    def test_many_minus_add_op_float(self):
        input = """void main(){
            putFloat(1+2-2.2+12-14-11);
        }"""
        expect = "-12.2"
        self.assertTrue(TestCodeGen.test(input, expect, 512))

    def test_simple_mul_op(self):
        input = """void main(){
            putInt(12*4);
        }"""
        expect = "48"
        self.assertTrue(TestCodeGen.test(input, expect, 513))

    def test_simple_div_op(self):
        input = """void main(){
            putInt(12/2);
        }"""
        expect = "6"
        self.assertTrue(TestCodeGen.test(input, expect, 514))

    def test_mul_div_one_side_float(self):
        input = """void main(){
            putFloat(2.4/2*12);
        }"""
        expect = "14.400001"
        self.assertTrue(TestCodeGen.test(input, expect, 515))

    def test_mix_add_minus_mul_div(self):
        input = """void main(){
            putInt(3+2*12-12/(3+4-5)*12);
        }"""
        expect = "-45"
        self.assertTrue(TestCodeGen.test(input, expect, 516))

    def test_simple_mod(self):
        input = """void main(){
            putInt(12%5);
        }"""
        expect = "2"
        self.assertTrue(TestCodeGen.test(input, expect, 517))

    def test_mix_mod(self):
        input = """void main(){
            putFloat(35%12+12-2.3*(3.2-2));
        }"""
        expect = "20.24"
        self.assertTrue(TestCodeGen.test(input, expect, 518))

    def test_or_op(self):
        input = """void main(){
            putBool(true||false);
        }"""
        expect = "true"
        self.assertTrue(TestCodeGen.test(input, expect, 519))

    def test_and_op(self):
        input = """void main(){
            putBool(true&&false);
        }"""
        expect = "false"
        self.assertTrue(TestCodeGen.test(input, expect, 520))

    def test_put_int_boolean_param(self):
        input = """void main(){
            putInt(false);
        }"""
        expect = "0"
        self.assertTrue(TestCodeGen.test(input, expect, 521))

    def test_mix_or_and_and_short_circuit_in_if(self):
        input = """void main(){
            int x;
            x = 2;
            if ( x < 100 || x > 200 && x != 3 ) x = 0; else x =1;
            putBool(x);
        }"""
        expect = "false"
        self.assertTrue(TestCodeGen.test(input, expect, 522))

    def test_simple_relational_op(self):
        input = """void main(){
            putBool(12>4);
        }"""
        expect = "true"
        self.assertTrue(TestCodeGen.test(input, expect, 523))

    def test_simple_relational_op_less_than_put_int(self):
        input = """void main(){
            putInt(12<2);
        }"""
        expect = "0"
        self.assertTrue(TestCodeGen.test(input, expect, 524))

    def test_many_relational_op(self):
        input = """void main(){
            putBool((3>2)>((1<-3)<=6));
        }"""
        expect = "false"
        self.assertTrue(TestCodeGen.test(input, expect, 525))

    def test_relational_op_with_float(self):
        input = """void main(){
            putBool(3.2>=2);
        }"""
        expect = "true"
        self.assertTrue(TestCodeGen.test(input, expect, 526))

    def test_equality_op(self):
        input = """void main(){
            putInt(true==false);
        }"""
        expect = "0"
        self.assertTrue(TestCodeGen.test(input, expect, 527))

    def test_mix_relational_op(self):
        input = """void main(){
            putBool(((2.2<3)>(3<2))<=2);
        }"""
        expect = "true"
        self.assertTrue(TestCodeGen.test(input, expect, 528))

    def test_mix_bool_op(self):
        input = """void main(){
            putBool((true||false)==2&&(2<=4.1));
        }"""
        expect = "false"
        self.assertTrue(TestCodeGen.test(input, expect, 529))

    def test_put_many_op(self):
        input = """void main(){
            putIntLn(true&&false);
            putFloat(.1+.2-.5*.9);
            putInt(7%2+2);
            putIntLn(3==(2+1));
            putBool(true&&false);
            putString("str");
        }"""
        expect = """0\n-0.1499999831\nfalsestr"""
        self.assertTrue(TestCodeGen.test(input, expect, 530))

    def test_put_many_relational_op(self):
        input = """void main(){
            putBool(1.2 > 1.2);
            putIntLn(1.2 < 1.2);
            putBool(1.2 >= 1.2);
            putBool(1.2 <= 1.2);
        }"""
        expect = """false0\ntruetrue"""
        self.assertTrue(TestCodeGen.test(input, expect, 531))

    def test_put_many_equality_op(self):
        input = """void main(){
            putBoolLn(1.2 == 1.2);
            putBool(1.2 != 1.2);
        }"""
        expect = """true\nfalse"""
        self.assertTrue(TestCodeGen.test(input, expect, 532))

    def test_simple_var_decl_assign(self):
        input = """
        int i;
        void main(){
            i=3;
            putInt(i);
        }"""
        expect = "3"
        self.assertTrue(TestCodeGen.test(input, expect, 533))

    def test_decl_after_use_in_global(self):
        input = """void main(){
            fl=2.1;
            putFloat(fl);
        }
        float fl;"""
        expect = "2.1"
        self.assertTrue(TestCodeGen.test(input, expect, 534))

    def test_assign_in_put(self):
        input = """void main(){
            putFloat(fl=2.1);
        }
        float fl;"""
        expect = "2.1"
        self.assertTrue(TestCodeGen.test(input, expect, 535))

    def test_many_var_op(self):
        input = """void main(){
            a=2;
            b=3;
            c=a*b+b%a;
            putFloat(c+b);
        }
        int a, b;
        float c;"""
        expect = "10.0"
        self.assertTrue(TestCodeGen.test(input, expect, 536))

    def test_add_many_var_and_assign_string(self):
        input = """int a;
        float b;
        void main(){
            a=5;
            a;
            b=5.5;
            c=6.3;
            b=a+c;
            b=c+b;
            putFloat(b);
            string str;
            str = "testString";
            putString(str);
        }
        float c;"""
        expect = "17.6testString"
        self.assertTrue(TestCodeGen.test(input, expect, 537))

    def test_assign_and_add_op(self):
        input = """void main(){
            putInt((a=5)+4);
            3;
            a+3;
        }
        int a;"""
        expect = "9"
        self.assertTrue(TestCodeGen.test(input, expect, 538))

    def test_complex_assign_and_others(self):
        input = """void main(){
            4*2;
            putBool((((a=3)-1)*3.2)<=((b=2.2)+3));
        }
        int a;
        float b;"""
        expect = "false"
        self.assertTrue(TestCodeGen.test(input, expect, 539))

    def test_put_float_int_param(self):
        input = """void main(){
            0||3;
            putFloat(3);
        }"""
        expect = "3.0"
        self.assertTrue(TestCodeGen.test(input, expect, 540))

    def test_negative_op(self):
        input = """void main(){
            putIntLn(-1);
            putInt((2+3)*-2);
        }"""
        expect = "-1\n-10"
        self.assertTrue(TestCodeGen.test(input, expect, 541))

    def test_not_op(self):
        input = """void main(){
            putBoolLn(!true);
            putBool(!(3.2<2));
        }"""
        expect = "false\ntrue"
        self.assertTrue(TestCodeGen.test(input, expect, 542))

    def test_many_negative_op(self):
        input = """
        float fl;
        void main(){
            fl = 4.0/5*12/34.2 - 3 + 99/4 - -----4*7 - ----3 - ---- 13;
            putFloat(fl);
        }"""
        expect = "33.2807"
        self.assertTrue(TestCodeGen.test(input, expect, 543))
    
    def test_decl_in_func(self):
        input = """void main(){
            float fl;
            int i;
            i = 1;
            fl = -i;
            putFloatLn(fl);
            int a;
            a;
            a = 12%(i+4);
            putFloat(a);
        }
        float fl;"""
        expect = "-1.0\n2.0"
        self.assertTrue(TestCodeGen.test(input, expect, 544))

    def test_many_put_line(self):
        input = """void main(){
            putFloat(fl=2.1);
            putLn();
            putLn();
            putLn();
            putLn();
            putLn();
            putBool(fl>2);
            putLn();
            putLn();
        }
        float fl;"""
        expect = "2.1\n\n\n\n\ntrue\n\n"
        self.assertTrue(TestCodeGen.test(input, expect, 545))

    def test_var_decl_in_block(self):
        input = """void main(){
            {
                int b;
                {
                    b = 4;
                    int a;
                    {
                        a = 5;
                        int i;
                        i = 3;
                        putFloatLn(5%3);
                        putFloat(b-a-i);
                    }
                }
            }
        }"""
        expect = "2.0\n-4.0"
        self.assertTrue(TestCodeGen.test(input, expect, 546))

    def test_complex_func_call(self):
        input = """boolean boo() {
            a = 2;
            if(a==2)
                putStringLn(str());
            fl = 3;
            return flo() > fl;
        }
        int a;
        int foo(){
            a = 3;
            return a;
        }
        float flo(){ 
            putIntLn(foo());
            return fl+1;
        }
        void main(){ 
            putBool(boo()); 
        }
        string str() {
            return "hello";
        }
        float fl;"""
        expect = "hello\n3\ntrue"
        self.assertTrue(TestCodeGen.test(input, expect, 547))

    def test_call_func_and_return(self):
        input = """void main(){
            putInt(foo());
        }
        int foo(){
            return 12;
        }"""
        expect = "12"
        self.assertTrue(TestCodeGen.test(input, expect, 548))

    def test_simple_local_array(self):
        input = """void main(){
            int a[4];
            a[2] = 5;
            putInt(a[2]);
        }"""
        expect = "5"
        self.assertTrue(TestCodeGen.test(input, expect, 549))

    def test_decl_var_global_same_name_with_array_local(self):
        input = """void main(){
            float a[10];
            a[6] = 12;
            putFloat(a[6]);
        }
        int a;"""
        expect = "12.0"
        self.assertTrue(TestCodeGen.test(input, expect, 550))

    def test_many_array_assign(self):
        input = """void main(){
            a[4] = 5;
            int b[4];
            b[3] = a[4] + 12;
            putIntLn(b[3]);
            int c[3];
            c[1] = b[3]*a[4];
            putInt(c[1]);
        }
        int a[5];"""
        expect = "17\n85"
        self.assertTrue(TestCodeGen.test(input, expect, 551))

    def test_simple_call_int_func(self):
        input = """void main(){
            putInt(foo(10));
        }
        int foo(int a){
            return a;
        }"""
        expect = "10"
        self.assertTrue(TestCodeGen.test(input, expect, 552))

    def test_string_call_func(self):
        input = """void main(){
            putString(foo("553"));
        }
        string foo(string a){
            return a;
        }"""
        expect = "553"
        self.assertTrue(TestCodeGen.test(input, expect, 553))
    
    def test_bool_call_func(self):
        input = """void main(){
            putBool(foo(1));
        }
        boolean foo(int a){
            return a;
        }"""
        expect = "true"
        self.assertTrue(TestCodeGen.test(input, expect, 554))

    def test_many_call_func(self):
        input = """int foo1(){
            int a;
            a = 5;
            return a;
        }
        float foo2(int a){
            return foo1()+a;
        }
        void main(){
            putIntLn(foo3());
            putFloat(foo2(3));
        }
        boolean foo3(){
            return true;
        }"""
        expect = "1\n8.0"
        self.assertTrue(TestCodeGen.test(input, expect, 555))

    def test_call_func_in_op(self):
        input = """void main(){
            int f;
            f = foo1();
            putFloat(foo2(5)*3+f);
        }
        int foo1(){
            int a;
            a = 5;
            return a;
        }
        float foo2(int a){
            return foo1()+a;
        }"""
        expect = "35.0"
        self.assertTrue(TestCodeGen.test(input, expect, 556))

    def test_simple_array_param(self):
        input = """void main(){
            int a[3];
            a[0] = 2;
            putInt(foo(a));
        }
        int foo(int a[]){
            return a[0];
        }"""
        expect = "2"
        self.assertTrue(TestCodeGen.test(input, expect, 557))

    def test_simple_output_array(self):
        input = """void main(){
            int a[3];
            a[1] = 12;
            putInt(foo(a)[1]);
        }
        int[] foo(int a[]){
            return a;
        }"""
        expect = "12"
        self.assertTrue(TestCodeGen.test(input, expect, 558))

    def test_mix_many_array_pointer_normal(self):
        input = """void main(){
            float a, b[4];
            a = 5;
            b[0] = a;
            putFloatLn(b[0]);
            putFloat(foo(a, b)[1]);
        }
        float[] foo(float a, float b[]){
            b[1] = a - 12;
            return b;
        }"""
        expect = "5.0\n-7.0"
        self.assertTrue(TestCodeGen.test(input, expect, 559))

    def test_simple_if(self):
        input = """void main(){
            if(true)
                putFloat(12);
        }"""
        expect = """12.0"""
        self.assertTrue(TestCodeGen.test(input, expect, 560))

    def test_if_label_in_else(self):
        input = """void main(){
            if(false)
                putFloat(12);
            else
                putInt(1);
        }"""
        expect = """1"""
        self.assertTrue(TestCodeGen.test(input, expect, 561))

    def test_relational_op_in_if_condi(self):
        input = """void main(){
            if(12>4)
                putFloatLn(3);
            putInt(3);
        }"""
        expect = """3.0\n3"""
        self.assertTrue(TestCodeGen.test(input, expect, 562))

    def test_var_relational_op_in_if(self):
        input = """
        float fl;
        void main(){
            fl = 2;
            if(fl==2)
                putFloatLn(fl);
            else
                putIntLn(21);
            putInt(3);
        }"""
        expect = "2.0\n3"
        self.assertTrue(TestCodeGen.test(input, expect, 563))
    
    def test_many_stmt_in_if(self):
        input = """void main(){
            fl = 12; 
            if(-1.2>3){
                putInt(43);
                fl = fl - 33;
                putFloat(fl);
            } else {
                putFloatLn(fl);
                putInt(12);
            }
        }
        float fl;"""
        expect = "12.0\n12"
        self.assertTrue(TestCodeGen.test(input, expect, 564))

    def test_array_in_if(self):
        input = """void main(){
            float fl[2];
            fl[0] = 2;
            if(fl[0]>0){
                int i[1];
                i[0] = 3;
                putInt(i[0]);
            }
        }"""
        expect = "3"
        self.assertTrue(TestCodeGen.test(input, expect, 565))

    def test_many_block_in_if(self):
        input = """void main(){
            {
                int b;
                {
                    b = 4;
                    if(b != 0){
                        int a;
                        {
                            a = 5;
                            int i;
                            i = 3;
                            putFloatLn(5%3);
                            putFloat(b-a-i);
                        }
                    } else 
                        putInt(0);
                }
            }
        }"""
        expect = "2.0\n-4.0"
        self.assertTrue(TestCodeGen.test(input, expect, 566))

    def test_many_assign_in_if(self):
        input = """
        void main(){
            int a[3];
            a[0] = 2;
            if(true)
                a[0] = a[0] = a[0] + 2;
            putInt(a[0]);
        }"""
        expect = "4"
        self.assertTrue(TestCodeGen.test(input, expect, 567))

    def test_simple_dowhile(self):
        input = """void main(){
            do
                putInt(12);
            while(false);
        }"""
        expect = "12"
        self.assertTrue(TestCodeGen.test(input, expect, 568))

    def test_many_stmt_in_dowhile(self):
        input = """void main(){
            do{
                int i[7];
                i[5] = 3;
                i[1] = 2;
                putInt(i[5]*i[1]);
            }
            while(false);
        }"""
        expect = "6"
        self.assertTrue(TestCodeGen.test(input, expect, 569))

    def test_loop_many_time_in_dowhile(self):
        input = """void main(){
            check = 12;
            do{
                int i[7];
                i[1] = 3;
                i[2] = 7;
                putIntLn(i[2]*i[1]);
                check = check + 1;
            }
            while(check < 15);
        }
        int check;"""
        expect = "21\n21\n21\n"
        self.assertTrue(TestCodeGen.test(input, expect, 570))

    def test_more_complex_loop_dowhile(self):
        input = """void main(){
            int check, condi;
            check = 12;
            condi = 1;
            do{
                i[1] = 3;
                i[2] = 7;
                putIntLn((i[2]-i[1])/2 * (condi=condi*2));
            }
            while(check > condi);
        }
        int i[7];"""
        expect = "4\n8\n16\n32\n"
        self.assertTrue(TestCodeGen.test(input, expect, 571))

    def test_break_in_dowhile(self):
        input = """void main(){
            check = 12;
            do{
                int i[7];
                i[1] = 3;
                i[2] = 7;
                putIntLn(i[2]*i[1]);
                check = check + 1;
                break;
            }
            while(check < 15);
            putInt(check);
        }
        int check;"""
        expect = "21\n13"
        self.assertTrue(TestCodeGen.test(input, expect, 572))

    def test_if_in_dowhile(self):
        input = """void main(){
            check = 12;
            do{
                int i[7];
                i[1] = 3;
                i[2] = 7;
                putIntLn(i[2]*i[1]);
                check = check + 1;
                if(check == 14)
                    break;
            }
            while(check < 15);
            putInt(check);
        }
        int check;"""
        expect = "21\n21\n14"
        self.assertTrue(TestCodeGen.test(input, expect, 573))
    
    def test_continue_in_dowhile(self):
        input = """void main(){
            check = 12;
            do{
                check = check + 1;
                if(check == 14)
                    continue;
                int i[7];
                i[1] = 3;
                i[2] = 7;
                putIntLn(i[2]*i[1]);
            }
            while(check < 15);
            putInt(check);
        }
        int check;"""
        expect = "21\n21\n15"
        self.assertTrue(TestCodeGen.test(input, expect, 574))

    def test_simple_for(self):
        input = """void main(){
            int i;
            for(i=0; i<5; i=i+1)
                putIntLn(i);
            putInt(i);
        }"""
        expect = "0\n1\n2\n3\n4\n5"
        self.assertTrue(TestCodeGen.test(input, expect, 575))

    def test_many_block_in_for(self):
        input = """void main(){
            {
                int b;
                for(b=1; b<12; b=b*2){
                    putIntLn(b);
                    if(b != 0){
                        int a;
                        {
                            a = 5;
                            int i;
                            i = 3;
                            putFloatLn(5%3);
                            putFloatLn(-a-i);
                        }
                    } else 
                        putInt(0);
                }
            }
        }"""
        expect = "1\n2.0\n-8.0\n2\n2.0\n-8.0\n4\n2.0\n-8.0\n8\n2.0\n-8.0\n"
        self.assertTrue(TestCodeGen.test(input, expect, 576))

    def test_break_in_for(self):
        input = """void main(){
            int a[3];
            for(a[1]=0; a[1]<1000; a[1]=a[1]+a[0]){
                if(a[1] > 7)
                    break;
                putIntLn(a[1]);
                a[0] = a[1] + 2;
            }
            putInt(a[0]);
        }"""
        expect = "0\n2\n6\n8"
        self.assertTrue(TestCodeGen.test(input, expect, 577))

    def test_continue_in_for(self):
        input = """void main(){
            int a[3];
            for(a[1]=0; a[1]<20; a[1]=a[1]+a[0]){
                a[0] = a[1] + 2;
                if(a[1] > 7)
                    continue;
                putIntLn(a[1]);
            }
            putInt(a[0]);
        }"""
        expect = "0\n2\n6\n16"
        self.assertTrue(TestCodeGen.test(input, expect, 578))

    def test_complex_if(self):
        input = """void main(){
            int a, b;
            a = 2;
            if(a != 2){ 
                {
                    putInt(a); // 2
                }
            } else {
                b = 2;
                if(a>b)
                    putInt(b*a); // 4
                else
                    if(a < b)
                        putInt(a-b); // 0
                    else
                        putInt(a/b); // 1
            } 
        }"""
        expect = "1"
        self.assertTrue(TestCodeGen.test(input, expect, 579))

    def test_more_complex_dowhile(self):
        input = """void main(){
            check = 12;
            int a;
            do{
                do
                    {
                        a = 2;
                        do
                            {
                                putIntLn(a=a*2-1);
                            }
                        while(a < 5);
                    }
                    break;
                while(a != 100);
                putLn();
                a = 2;
                do
                    {
                        putIntLn(a=a*2-1);
                    }
                while(a < 5);
                check = check + 1;
            }
            while(check < 15);
        }
        int check;"""
        expect = "3\n5\n\n3\n5\n3\n5\n\n3\n5\n3\n5\n\n3\n5\n"
        self.assertTrue(TestCodeGen.test(input, expect, 580))

    def test_complex_for(self):
        input = """void main(){
            int a, b;
            {
                {
                    {
                        for(a=0; a<10; a=a+1)
                            for(b=5; b<50; b=b+10){
                                putFloatLn(b-a);
                                a=b;
                                if(a > 30)
                                    break;
                            }
                    }
                }
                {
                    for(b=0; b<12; b=b*2){
                        int c;
                        c = 10;
                        a = (c+b)/2;
                        putIntLn(b=a);
                    }
                }
            }
        }"""
        expect = "5.0\n10.0\n10.0\n10.0\n5\n10\n"
        self.assertTrue(TestCodeGen.test(input, expect, 581))

    def test_dowhile_if_for(self):
        input = """void main(){
            check = 5;
            if(check) {
                int a;
                a = 5;
                if(a)
                    do
                        for(a=0; a<4; a=a+1)
                            putIntLn(a);
                        putString("end");
                        if(a > 0)
                            break;
                    while(true);
            }
        }
        int check;"""
        expect = "0\n1\n2\n3\nend"
        self.assertTrue(TestCodeGen.test(input, expect, 582))

    def test_short_circuit_or_if_only(self):
        input = """void main(){
            int a,b,c;
            a=0;
            b=5;
            c=10;
            if(a>2||b<c||c>5)
                putInt(1);
        }"""
        expect = "1"
        self.assertTrue(TestCodeGen.test(input, expect, 583))
    
    def test_return_stop_dowhile_in_other_func(self):
        input = """void main(){
            putInt(foo());
        }
        int foo(){
            int b;
            b = 0;
            do
                b = b+1;
                if(b==3)
                    return b;
            while(b<5);
            return 1;
        }"""
        expect = "3"
        self.assertTrue(TestCodeGen.test(input, expect, 584))

    def test_short_circuit_with_endless_recursive(self):
        input = """void main(){
            int i;
            for(i=0; i>-1 || i<4 && i>1 || boo(); i=i+1)
                if(i>2 || i==0 || true && boo()){
                    putInt((i=3)+123);
                    break;
                }
        }
        boolean boo(){
            return boo();
        }"""
        expect = "126"
        self.assertTrue(TestCodeGen.test(input, expect, 585))

    def test_output_array_pointer_as_left_assign(self):
        input = """void main(){
            int a[5];
            foo(a)[2] = 3;
            putInt(a[2]);
        }
        int[] foo(int a[]){
            return a;
        }"""
        expect = "3"
        self.assertTrue(TestCodeGen.test(input, expect, 586))

    def test_short_circuit_and_in_for_in_dowhile(self):
        input = """void main(){
            int a;
            a = -5;
            int b, c;
            c = 0;
            do
                for(b=0; b<2 && a<5; b=b+1){
                    a = a + 1;
                    putIntLn(a);
                    c = c + 1;
                }
                a = -5;
            while(c<3 && a<5);
        }"""
        expect = "-4\n-3\n-4\n-3\n"
        self.assertTrue(TestCodeGen.test(input, expect, 587))

    def test_for_in_dowhile_break_condi_and_simple_array_global(self):
        input = """int a[3];
        void main(){
            int a;
            a = -5;
            int b;
            do
                for(b=0; b<3; b=b+1){
                    a = a+b;
                    putIntLn(a);
                }
                if(a>=5){
                    break;
                }
            while(true);
        }"""
        expect = "-5\n-4\n-2\n-2\n-1\n1\n1\n2\n4\n4\n5\n7\n"
        self.assertTrue(TestCodeGen.test(input, expect, 588))

    def test_complex_for_in_branch(self):
        input = """void main(){
            int a, b;
            a = 2;
            if(a != 2){ 
                {
                    putInt(a); // 2
                }
            } else {
                b = 2;
                if(a<=b)
                    for(a=2; a<=b; a=a+1){
                        b = 10;
                        putIntLn(b*a);
                    }
                else
                    if(a < b)
                        putInt(a-b); // 0
                    else
                        putInt(a/b); // 1
            } 
        }"""
        expect = "20\n30\n40\n50\n60\n70\n80\n90\n100\n"
        self.assertTrue(TestCodeGen.test(input, expect, 589))

    def test_many_array_global_decl(self):
        input = """int a[3], b[2];
        void main(){
            a[0] = b[1] = 2;
            x[3] = a[0] + b[1];
            y[5] = x[3] / a[0];
            putFloat(y[5]);
        }
        float x[4], y[7];"""
        expect = "2.0"
        self.assertTrue(TestCodeGen.test(input, expect, 590))

    def test_complex_mix_stmt_short_circuit_if_or(self):
        input = """void main(){ 
            int a,b;
            a = 2;
            b = 3;
            float fl;
            {
                fl = 3;
                if(a>b){
                    {
                        for(a=6; b<a; b=b+1){
                            if(fl>2.2)
                                a=b;
                        }
                    }
                } else {
                    do
                        fl = fl * a + b / fl;
                        if(a<b || a==b || b>1 || true || false)
                            putFloatLn(fl);
                        else 
                            putFloatLn(fl = fl -- 1);
                    while(fl<12.2);
                }
            }
        }"""
        expect = "7.0\n14.428572\n"
        self.assertTrue(TestCodeGen.test(input, expect, 591))

    def test_multiple_not_func(self):
        input = """void main(){
            int i;
            for(i=0; i<5; i=i+1){
                if(i>3)
                    putBoolLn(!!!!!!boo(false));
                else
                    putBoolLn(!!!!boo(true));
            }
        }
        boolean boo(boolean boo){
            return boo;
        }"""
        expect = "true\ntrue\ntrue\ntrue\nfalse\n"
        self.assertTrue(TestCodeGen.test(input, expect, 592))

    def test_return_true_via_odd_value(self):
        input = """void main(){
            int i;
            for(i=0; i<5; i=i+1){
                putBoolLn(boo(false, i));
            }
        }
        boolean boo(boolean boo, int i){
            if(i%2)
                return boo;
            else
                return !boo;
            return false;
        }"""
        expect = "true\nfalse\ntrue\nfalse\ntrue\n"
        self.assertTrue(TestCodeGen.test(input, expect, 593))
    
    def test_simple_recursive(self):
        input = """int i;
        void main(){
            i = 0;
            putInt(foo());
        }
        int foo(){
            if(i>3){
                return i;
            }
            i = i + 1;
            return foo();
        }"""
        expect = "4"
        self.assertTrue(TestCodeGen.test(input, expect, 594))

    def test_tail_call_optimal_short_circuit_if_and(self):
        input = """float foo(float a, float b){
            /* comment
            */
            if(a == 1 && a > 0)
                return b;
            else
                return foo(a-1, a*b);
            return 1;
        }
        void main(){
            putFloat(foo(8, 1));
        }"""
        expect = "40320.0"
        self.assertTrue(TestCodeGen.test(input, expect, 595))

    def test_return_via_idx_of_param(self):
        input = """int a[10];
            void main(){
            int i;
            i=0;
            a[0] = i;
            do
                i = i + 1;
                putIntLn(foo(a, i));
            while(a[0]<5);
        }
        int foo(int a[], int i){
            a[0] = a[0] + 1;
            a[i] = a[0] * 2;
            return a[i];
        }"""
        expect = "2\n4\n6\n8\n10\n"
        self.assertTrue(TestCodeGen.test(input, expect, 596))

    def test_factorial_prog(self):
        input = """int fact(int x){
            int fact, i;
            fact = 1;
            for(i=1; i<=x; i=i+1){
                fact = fact * i;
            }
            return fact;
        }
        void main(){
            for(a=2; a<15; a=a+1){
                putIntLn(fact(a));
            }
            putString("stop!");
        }
        int a;"""
        expect = "2\n6\n24\n120\n720\n5040\n40320\n362880\n3628800\n39916800\n479001600\n1932053504\n1278945280\nstop!"
        self.assertTrue(TestCodeGen.test(input, expect, 597))

    def test_fibonacci_prog(self):
        input = """void main(){
            int i, n1, n2, next;
            n2 = (n1=next=0)+1;
            for (i = 1; i <= 25; i=i+1){
                if(i == 1){
                    putString("first:");
                    putIntLn(n1);
                    continue;
                }
                if(i == 2){
                    putString("second:");
                    putIntLn(n2);
                    continue;
                }
                next = n1 + n2;
                n1 = n2;
                n2 = next;
                putIntLn(next);
            }
            return;
        }"""
        expect = "first:0\nsecond:1\n1\n2\n3\n5\n8\n13\n21\n34\n55\n89\n144\n233\n377\n610\n987\n1597\n2584\n4181\n6765\n10946\n17711\n28657\n46368\n"
        self.assertTrue(TestCodeGen.test(input, expect, 598))

    def test_complex_program(self):
        input = """boolean boo(boolean boo) {
            a = 2;
            if(a==2) {
                {
                    if(boo) {
                        for(a=0; boo; a=a+1){
                            return boo;
                        }
                    }
                    return boo;
                }
            }
            else 
                return boo;
            return boo;
        }
        int a;
        float flo() {
            do
                fl = 5;
                a = a + 2;
                if(a==2 && a>0) {
                    {
                        if(bool[3] || a < 5 && !bool[3]) {
                            for(a=0; bool[3]; a=a+1){
                                return -----1111121;
                            }
                        }
                        return fl;
                    }
                }
                else {
                    if(bool[3]) {
                        return fl*fl;
                    }
                }
            while(boo(bool[3]));
            return fl;
        }
        void main() {
            bool[3] = true;
            putBoolLn(boo(bool[3]));
            putFloat(flo());
        }
        float fl;
        boolean bool[5];"""
        expect = "true\n-1111121.0"
        self.assertTrue(TestCodeGen.test(input, expect, 599))
