package Q1;

public class Assistente extends Funcionario{
    
    public Assistente(String nome, String matricula, double salario_base) {
        super(nome, matricula, salario_base);
    }
    @Override
    public String exibeDados(){
        double salario_assist = super.getsalario_base() * 0.3;
    String dados = " Nome: " + super.getnome();
    dados+= " Matricula: " + super.getmatricula();
    dados+= " Salario: " + (super.getsalario_base() + salario_assist);
        return dados;
}

}
