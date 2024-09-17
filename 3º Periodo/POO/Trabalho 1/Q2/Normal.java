package Q2;

public class Normal extends Ingresso{
    
    public Normal(double valor) {
        super(valor);
    }
    

@Override
    public String imprimeValor(){
        String text = "Tipo do ingresso: Normal";
        text+= "valor: " +(super.getvalor());
    return text;
    }
}
