/*
 * Click nbfs://nbhost/SystemFileSystem/Templates/Licenses/license-default.txt to change this license
 * Click nbfs://nbhost/SystemFileSystem/Templates/UnitTests/JUnit5TestClass.java to edit this template
 */

import static org.hamcrest.CoreMatchers.is;
import static org.hamcrest.MatcherAssert.assertThat;
import static org.hamcrest.Matchers.closeTo;
import org.junit.jupiter.api.AfterEach;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

/**
 *
 * @author stefa
 */
public class InvoiceItemTest {
    
    private InvoiceItem item;
    
    public InvoiceItemTest() {
    }
    
    @BeforeEach
    public void setUp() {
        item = new InvoiceItem();
        item.setProductName("Polkadot Widget");
        item.setSalePrice(0.1);
        item.setQuantityPurchased(0.2);
    }
    
    @AfterEach
    public void tearDown() {
    }

    @Test
    public void testGetItemTotal() {
        Double result = item.getItemTotal();
        assertThat(result, is(closeTo(0.02, 0.0001)));
    }
    
}
