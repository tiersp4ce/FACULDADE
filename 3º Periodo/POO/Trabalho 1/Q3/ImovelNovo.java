package Q3;

public class ImovelNovo extends Imovel{

private double adici;

//Construtor
    
    public ImovelNovo(String endereco, double preco, double adici) {
        super(endereco, preco);
        this.adici = adici;
    }
    
//get e set
public double getadici(){
    return adici;
}

public void setadici(double adici){
    this.adici = adici;
}



@Override
    public String impressao(){
        String text = "Tipo de Imovel: Novo ";
        text+= "Preco: " +(super.getpreco() + getadici());
        text+= "Endereco: " +super.getendereco();
    return text;

}



}
