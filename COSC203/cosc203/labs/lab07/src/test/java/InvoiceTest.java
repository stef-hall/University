/*
 * Click nbfs://nbhost/SystemFileSystem/Templates/Licenses/license-default.txt to change this license
 * Click nbfs://nbhost/SystemFileSystem/Templates/UnitTests/JUnit5TestClass.java to edit this template
 */

import org.junit.jupiter.api.AfterEach;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;
import java.time.LocalDate;

import static org.hamcrest.MatcherAssert.assertThat;
import static org.hamcrest.Matchers.closeTo;
import static org.hamcrest.Matchers.hasItem;
import static org.hamcrest.Matchers.hasSize;
import static org.hamcrest.Matchers.is;
import static org.hamcrest.Matchers.not;

import org.junit.jupiter.api.AfterEach;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;

public class InvoiceTest {

	private Invoice invoice;
	private InvoiceItem item1;
	private InvoiceItem item2;
	private InvoiceItem item3;

	@BeforeEach
	public void setUp() {
		invoice = new Invoice();
		invoice.setCustomerName("Doris Delores");
		invoice.setCustomerAddress("123 Some Street, Some where");
		invoice.setDate(LocalDate.now());

		item1 = new InvoiceItem();
		item1.setProductName("Polkadot Widget");
		item1.setSalePrice(0.1);
		item1.setQuantityPurchased(0.2);

		item2 = new InvoiceItem();
		item2.setProductName("Dodgy Doohicky");
		item2.setSalePrice(1.0);
		item2.setQuantityPurchased(2.0);

		item3 = new InvoiceItem();
		item3.setProductName("Fuzzy Widget");
		item3.setSalePrice(1.1);
		item3.setQuantityPurchased(2.2);

		invoice.addItem(item1);
		invoice.addItem(item2);

		//intentionally not adding item3 since it is added in testAddItem
	}

	@AfterEach
	public void tearDown() {
            invoice.removeItem(item1);
            invoice.removeItem(item2);
                invoice.removeItem(item3);
	}

	@Test
	public void testAddItem() {
		// make sure that item3 does not already exist
		assertThat(invoice.getItems(), not(hasItem(item3)));
		assertThat(invoice.getItems(), hasSize(2));

		// add it
		invoice.addItem(item3);

		// check that it was added
		assertThat(invoice.getItems(), hasItem(item3));
		assertThat(invoice.getItems(), hasSize(3));
                
	}

	@Test
	public void testRemoveItem() {
		// make sure that item1 does already exist
		assertThat(invoice.getItems(), hasItem(item1));
		assertThat(invoice.getItems(), hasSize(2));

		// delete it
		invoice.removeItem(item1);

		// make sure that it is gone
		assertThat(invoice.getItems(), not(hasItem(item1)));
		assertThat(invoice.getItems(), hasSize(1));
	}

	@Test
	public void testGetTotal() {
		assertThat(invoice.getTotal(), is(closeTo(2.02, 0.0001)));
	}

}