#!/usr/bin/env python

from abc import ABC, abstractmethod
from typing import Optional


class TaxCalculator(ABC):
    """
    Base class for tax calculators.

    Attributes:
        tax_rate (float): The tax rate to use for calculations.
    """

    def __init__(self, tax_rate: float):
        """
        Initializes the tax calculator with a given tax rate.

        Args:
            tax_rate (float): The tax rate to use for calculations.
        """
        self.tax_rate = tax_rate

    @abstractmethod
    def calculate_tax(self, salary: float) -> float:
        """
        Calculates the tax amount based on the provided salary and tax rate.

        Args:
            salary (float): The salary to calculate tax for.

        Returns:
            float: The calculated tax amount.
        """
        pass


class StandardTaxCalculator(TaxCalculator):
    """
    A standard tax calculator that uses a fixed tax rate of 25%.
    """

    def __init__(self):
        super().__init__(tax_rate=0.25)

    def calculate_tax(self, salary: float) -> float:
        """
        Calculates the tax amount using the parent's calculation.

        Args:
            salary (float): The salary to calculate tax for.

        Returns:
            float: The calculated tax amount.
        """
        return salary * self.tax_rate


class CustomTaxCalculator(TaxCalculator):
    """
    A custom tax calculator that uses a fixed tax rate of 30%.
    """

    def __init__(self):
        super().__init__(tax_rate=0.30)

    def calculate_tax(self, salary: float) -> float:
        """
        Calculates the tax amount using the parent's calculation.

        Args:
            salary (float): The salary to calculate tax for.

        Returns:
            float: The calculated tax amount.
        """
        return salary * self.tax_rate


class Employee:
    """
    Represents an employee with a name, salary, and assigned tax calculator.
    """

    def __init__(self, name: str, salary: float, tax_calculator: TaxCalculator):
        """
        Initializes the employee with a given name, salary, and tax calculator.

        Args:
            name (str): The employee's name.
            salary (float): The employee's salary.
            tax_calculator (TaxCalculator): The tax calculator to use for
            calculations.

        Raises:
            TypeError: If the provided tax calculator is not an instance of
            TaxCalculator. """
        self.name = name
        self.salary = salary
        if not isinstance(self.tax_calculator, TaxCalculator):
            raise TypeError(
                "tax_calculator must be an instance of TaxCalculator")
        self.tax_calculator = tax_calculator

    def calculate_tax(self) -> float:
        """
        Calculates the employee's tax amount using their assigned tax
        calculator.

        Returns:
            float: The calculated tax amount.
        """
        return self.tax_calculator.calculate_tax(self.salary)


class TaxCalculatorFactory:
    """
    A factory class for creating instances of tax calculators.
    """

    def create_tax_calculator(
            self, tax_type: Optional[str] = "standard") -> TaxCalculator:
        """
        Creates an instance of a tax calculator based on the provided tax type.

        Args:
            tax_type (Optional[str]): The tax type to use for calculations.
            Defaults to "standard".

        Returns:
            TaxCalculator: An instance of the created tax calculator.

        Raises:
            ValueError: If the provided tax type is unknown.
        """
        if tax_type == "standard":
            return StandardTaxCalculator()
        elif tax_type == "custom":
            return CustomTaxCalculator()
        else:
            raise ValueError(f"Unknown tax type: {tax_type}")


# --- Usage ---
if __name__ == "__main__":
    tax_calculator_factory = TaxCalculatorFactory()

    # Use the factory to get instances of tax calculators
    standard_tax_calculator = tax_calculator_factory.create_tax_calculator(
        "standard")
    employee_standard = Employee("John Doe", 50000, standard_tax_calculator)
    standard_tax_amount = employee_standard.calculate_tax()
    print(
        f"Standard tax amount for {employee_standard.name}: ${standard_tax_amount:.2f}")

    custom_tax_calculator = tax_calculator_factory.create_tax_calculator(
        "custom")
    employee_custom = Employee("Jane Smith", 60000, custom_tax_calculator)
    custom_tax_amount = employee_custom.calculate_tax()
    print(
        f"Custom tax amount for {employee_custom.name}: ${custom_tax_amount:.2f}")
