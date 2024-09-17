package Q1;

public class Gerente extends Funcionario{
    
    public Gerente(String nome, String matricula, double salario_base) {
        super(nome, matricula, salario_base);
    }
    @Override
    public String exibeDados(){
        double salario_gerente = super.getsalario_base() * 0.5;
    String dados = " Nome: " + super.getnome();
    dados+= " Matricula: " + super.getmatricula();
    dados+= " Salario: " + (super.getsalario_base() + salario_gerente);
        return dados;
}
    
}

