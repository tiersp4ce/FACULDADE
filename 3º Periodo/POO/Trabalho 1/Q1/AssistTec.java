package Q1;

public class AssistTec extends Assistente{
    
    public AssistTec(String nome, String matricula, double salario_base) {
        super(nome, matricula, salario_base);
    }
    
@Override
    public String exibeDados(){
    double add = getsalario_base() * 0.05 ;
    
    double salario_assist = (super.getsalario_base() * 0.3) + add;
    String dados = " Nome: " + super.getnome();
    dados+= " Matricula: " + super.getmatricula();
    dados+= " Salario: " + (super.getsalario_base() + salario_assist);
        return dados;
}    
    
    
    
}
