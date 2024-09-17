package Q1;

public class Funcionario {

private String nome;    
private String matricula;
private Double salario_base;
        
//Construtor
public Funcionario (String nome,String matricula, double salario_base){
this.nome = nome;
this.matricula = matricula;
setsalario_base(salario_base);


}

//Get e Set

public String getnome(){
    return nome;
}
public void setnome(String nome){
    this.nome = nome;
}
public String getmatricula(){
    return matricula;
}
public void setmatricula(String matricula){
    this.matricula = matricula;
}        
public double getsalario_base(){
    return salario_base;
}
public void setsalario_base(double salario_base){
    this.salario_base = salario_base;
    
    if (salario_base <=0){
        throw new IllegalArgumentException(
        "O salário nao pode ser 0");
    }
}        
        
public String exibeDados(){
    return null;
}

}
