from decimal import Decimal, ROUND_HALF_UP

def round_half_up(value: float, ndigits: int = 2):
    # 基于 Decimal 的更精确四舍五入
    
    if(value is None): 
        return 0.0
    
    d = Decimal(str(value))
    
    quantize_str = f"0.{'0' * (ndigits - 1)}1" if ndigits > 0 else "1"
    
    return float(d.quantize(Decimal(quantize_str), rounding=ROUND_HALF_UP))