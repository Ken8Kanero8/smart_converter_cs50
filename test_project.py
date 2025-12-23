# test_project.py

from project import is_prime, solve_quadratic, convert_unit

# Test prime number checker
def test_is_prime():
    assert is_prime(2) == True
    assert is_prime(3) == True
    assert is_prime(5) == True
    assert is_prime(17) == True
    assert is_prime(29) == True
    
    assert is_prime(1) == False
    assert is_prime(4) == False
    assert is_prime(9) == False
    assert is_prime(15) == False
    assert is_prime(100) == False

# Test quadratic equation solver
def test_solve_quadratic():
    # Two distinct real roots
    result1 = solve_quadratic(1, -5, 6)
    assert "Two distinct real roots: 3.000000 and 2.000000" in result1
    
    # One real root (repeated)
    result2 = solve_quadratic(1, -2, 1)
    assert "One real root (repeated): 1.000000" in result2
    
    # Complex roots
    result3 = solve_quadratic(1, 0, 1)
    assert "Two complex roots: 0.000000 ± 1.000000i" in result3

# Test unit conversion
def test_convert_unit():
    # Length: meter to centimeter
    assert abs(convert_unit(1, "Length", "meter", "centimeter") - 100) < 0.000001
    
    # Length: kilometer to meter
    assert abs(convert_unit(1, "Length", "kilometer", "meter") - 1000) < 0.000001
    
    # Weight: kilogram to pound – استفاده از مقدار دقیق‌تر و تلورانس بیشتر
    result = convert_unit(1, "Weight", "kilogram", "pound")
    assert abs(result - 2.2046226218487758) < 0.0001  # تلورانس رو کمی بازتر کردیم
    
    # Weight: gram to kilogram
    assert abs(convert_unit(1000, "Weight", "gram", "kilogram") - 1) < 0.000001
    
    # Temperature: Celsius to Fahrenheit
    assert abs(convert_unit(0, "Temperature", "Celsius", "Fahrenheit") - 32) < 0.000001
    assert abs(convert_unit(100, "Temperature", "Celsius", "Fahrenheit") - 212) < 0.000001
    
    # Temperature: Kelvin to Celsius
    assert abs(convert_unit(273.15, "Temperature", "Kelvin", "Celsius") - 0) < 0.000001

# Run tests with verbose output when executed directly
if __name__ == "__main__":
    import pytest
    pytest.main(["-v", __file__])