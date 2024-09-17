package Q3;

public class ImovelVelho extends Imovel{

private double descont;

//Construtor
    
    public ImovelVelho(String endereco, double preco, double descont) {
        super(endereco, preco);
        this.descont = descont;
    }
    
//get e set
public double getdescont(){
    return descont;
}

public void setdescont(double descont){
    this.descont = descont;
}



@Override
    public String impressao(){
        String text = "Tipo de Imovel: Velho ";
        text+= "Preco: " +(super.getpreco() - getdescont());
        text+= "Endereco: " +super.getendereco();
    return text;

}



}
