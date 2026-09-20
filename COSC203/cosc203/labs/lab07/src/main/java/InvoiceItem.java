
import java.time.LocalDate;

/*
 * Click nbfs://nbhost/SystemFileSystem/Templates/Licenses/license-default.txt to change this license
 * Click nbfs://nbhost/SystemFileSystem/Templates/Classes/Class.java to edit this template
 */

/**
 *
 * @author stefa
 */
public class InvoiceItem {
    String productName;
    Double salePrice;
    Double quantityPurchased;

    public String getProductName() {
        return productName;
    }

    public Double getSalePrice() {
        return salePrice;
    }

    public Double getQuantityPurchased() {
        return quantityPurchased;
    }

    public void setProductName(String productName) {
        this.productName = productName;
    }

    public void setSalePrice(Double salePrice) {
        this.salePrice = salePrice;
    }

    public void setQuantityPurchased(Double quantityPurchased) {
        this.quantityPurchased = quantityPurchased;
    }
    
    public Double getItemTotal() {
        return this.salePrice * this.quantityPurchased;
    }

    
}
