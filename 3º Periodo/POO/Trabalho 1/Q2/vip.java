package Q2;

public class vip extends Ingresso{

private double add;

//Construtor
public vip(double valor, double add) {
        super(valor);
    this.add = add;
    }

//get e super
public double getadd(){
    return add;
}    
public void setadd(double add){
    this.add = add;
}

    
    
@Override
    public String imprimeValor(){
        String text = "Tipo do ingresso: VIP";
        text+= "valor: " +(super.getvalor() + getadd());
    return text;

}
}
