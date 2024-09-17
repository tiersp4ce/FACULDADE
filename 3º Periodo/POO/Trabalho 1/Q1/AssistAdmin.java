package Q1;

public class AssistAdmin extends Assistente{

private String turno;
    
    public AssistAdmin(String nome, String matricula, double salario_base, String turno) {
        super(nome, matricula, salario_base);
    }
//Get e Set
public String getturno(){
    return turno;
}
public void setturno(String turno){
    this.turno = turno;
}
@Override
    public String exibeDados(){
    double add = 0;
        if ("noite".equals(getturno())){
        add = super.getsalario_base() * 0.15 ;
    }
        
        double salario_assist = (super.getsalario_base() * 0.3) + add;
    String dados = " Nome: " + super.getnome();
    dados+= " Matricula: " + super.getmatricula();
    dados+= " Salario: " + (super.getsalario_base() + salario_assist);
        return dados;
}    


}
