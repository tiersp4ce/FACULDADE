package Q2;


public class CamaroSup extends vip {
    
private String localizacao; 
    
//Construtor
public CamaroSup(String localizacao, double valor, double add) {
        super(valor, add);
        this.localizacao = localizacao;
    }

//get e set

public String getlocalizacao(){
    return localizacao;
}    
public void setlocalizacao(String localizacao){
    this.localizacao = localizacao;
}

@Override
    public String imprimeValor(){
        String text = "Tipo do Camarote: Superior ";
        text+= "Localizacao: " +getlocalizacao() ;
        text+= " valor: " +(super.getvalor() + getadd());
    return text;

}










}
