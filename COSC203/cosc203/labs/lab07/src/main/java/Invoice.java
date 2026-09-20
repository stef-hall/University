
import java.time.LocalDate;
import java.util.ArrayList;

/*
 * Click nbfs://nbhost/SystemFileSystem/Templates/Licenses/license-default.txt to change this license
 * Click nbfs://nbhost/SystemFileSystem/Templates/Classes/Class.java to edit this template
 */

/**
 *
 * @author stefa
 */
public class Invoice {
    private String customerName;
    private String customerAddress;
    private LocalDate date;
    private static ArrayList<InvoiceItem> items = new ArrayList<>();

    public String getCustomerName() {
        return customerName;
    }

    public String getCustomerAddress() {
        return customerAddress;
    }

    public LocalDate getDate() {
        return date;
    }

    public void setCustomerName(String customerName) {
        this.customerName = customerName;
    }

    public void setCustomerAddress(String customerAddress) {
        this.customerAddress = customerAddress;
    }

    public void setDate(LocalDate date) {
        this.date = date;
    }
    
    public void addItem(InvoiceItem item){
        items.add(item);
    }
    
    public void removeItem(InvoiceItem item){
        items.remove(item);
    }
    
    public double getTotal() {
        return items.stream().mapToDouble(item -> item.getItemTotal()).sum();
    }
    
    public ArrayList<InvoiceItem> getItems() {
        return items;
    }
}
