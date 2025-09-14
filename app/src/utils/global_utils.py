from decimal import Decimal


class GlobalUtils:

     @staticmethod
     def calculate_total_amount(tax: int,
                                discount: int,
                                subtotal: float,
                                ):
          temp_sub_total = subtotal
          sub_total_with_discount = (temp_sub_total - ((discount / 100) * subtotal))
          total_amount_with_tax = (sub_total_with_discount + (tax / 100) * sub_total_with_discount)
          return Decimal(total_amount_with_tax).quantize(Decimal("0.00"))



