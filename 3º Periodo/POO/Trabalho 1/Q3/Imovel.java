package Q3;

public class Imovel {

private String endereco;
private double preco;

//Construtor

public Imovel(String endereco, double preco){
    this.endereco = endereco;
    this.preco = preco;

}

//get e set 

public String getendereco(){
    return endereco;
}

public void setendereco(String endereco){
    this.endereco = endereco;
}

public double getpreco(){
    return preco;
}

public void setpreco(double preco){
    this.preco = preco;
}

public String impressao(){
    return null;

}

}
