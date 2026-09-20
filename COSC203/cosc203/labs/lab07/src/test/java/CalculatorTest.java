/*
 * Click nbfs://nbhost/SystemFileSystem/Templates/Licenses/license-default.txt to change this license
 * Click nbfs://nbhost/SystemFileSystem/Templates/UnitTests/JUnit5TestClass.java to edit this template
 */

import static org.hamcrest.CoreMatchers.is;
import static org.hamcrest.MatcherAssert.assertThat;
import org.junit.jupiter.api.AfterEach;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

/**
 *
 * @author stefa
 */
public class CalculatorTest {
    
    private Calculator calc;
    
    public CalculatorTest() {
    }
    
    
    @BeforeEach
    public void setUp() {
        this.calc = new Calculator();
    }
    
    @AfterEach
    public void tearDown() {
    }

    @Test
    public void testAdd() {
        assertThat(calc.add(1, 2), is(3));
        assertThat(calc.add(5, -4), is(1));
        assertThat(calc.add(-5, 4), is(-1));
        assertThat(calc.add(4, -8), is(-4));
        assertThat(calc.add(-1, -5), is(-6));
    }

    @Test
    public void testMultiply() {
    }
    
}
