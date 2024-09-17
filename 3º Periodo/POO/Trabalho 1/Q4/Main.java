package Q4;

import Q1.*;
import Q2.*;
import Q3.*;
import java.util.Scanner;

public class Main {
    public static void main(String[] args){

//Questao A
    AssistAdmin administrativo = new AssistAdmin("Andre Freire", "PI2020003", 2000, "Noite");
    AssistTec tecnico = new AssistTec ("Hitalo", "PI9020002", 1700);
    System.out.println(administrativo.exibeDados());
    System.out.println(tecnico.exibeDados());
    
//Questao B
    try {
        Scanner scanner = new Scanner(System.in);
        System.out.println("\nDigite 1 para Ingresso Normal ou 2 para Ingresso VIP:");
        int tipoIngresso = scanner.nextInt();

        Ingresso ingresso;
            
            if (tipoIngresso == 1) {
                ingresso = new Normal(100.00);
                ingresso.imprimeValor();
                System.out.println(ingresso.imprimeValor());
            } else if (tipoIngresso == 2) {
                System.out.println("Digite 1 para Camarote Superior ou 2 para Camarote Inferior:");
                int tipoCamarote = scanner.nextInt();
    
                if (tipoCamarote == 1) {
                    ingresso = new CamaroSup("Cima", 100.00, 50.00);
                    System.out.println(ingresso.imprimeValor());
                    System.out.println("Ingresso VIP Camarote Superior");
                } else if (tipoCamarote == 2) {
                    ingresso = new CamaroInfe("Baixo", 100.00, 30.00);
                    System.out.println(ingresso.imprimeValor());
                    System.out.println("Ingresso VIP Camarote Inferior");
                } else {
                    System.out.println("Opção inválida.");
                    return;
                }
            } else {
                System.out.println("Opção inválida.");
                return;
            }


            System.out.println("Escolha um Imovel \nVelho - 1\nNovo - 2\n");
            int tipo = scanner.nextInt(); 
            if (tipo == 1) {
                ImovelVelho velho = new ImovelVelho("Centro sul", 5000, 1500);
                System.out.println(velho.impressao());
            
            } else if (tipo == 2) {
                ImovelNovo Novo = new ImovelNovo("Centro norte", 5000, 1500);
                System.out.println(Novo.impressao());
            
        }
          
        } catch (Exception e) {
            System.err.println("Argumento invalido");
        }





    }
    


    
    
    
    
    }
