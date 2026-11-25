# 方案设计（plan.md）— Issue #1

## 根因
`total_cents()` 使用 `float(unit_price)`：`1.005` 在 IEEE 754 双精度下约为
`1.00499999999999989`，乘 100 后 `round()` 得 100（银行家舍入叠加），结算少 1 分。

## 方案
1. `from decimal import Decimal, ROUND_HALF_UP`。
2. 实现：
   ```python
   return int((Decimal(unit_price) * quantity * 100).quantize(Decimal("1"), rounding=ROUND_HALF_UP))
   ```
   - 字符串直构 `Decimal("1.005")` 精确等于 1.005，杜绝 float 误差；
   - 先算总额再舍到分（与现行语义一致，避免逐件舍入累积）；
   - `ROUND_HALF_UP` 四舍五入，半分边界（x.xx5）向上进位。

## 兼容性
签名 `total_cents(unit_price: str, quantity: int) -> int` 不变；合法十进制字符串契约不变（非法字符串抛 `decimal.InvalidOperation`，与现状异常行为同类，不新增语义）。

## 测试 seam
公开函数 `checkout.total_cents` —— 单元测试直接在该 seam 上验证（无需新建 seam）。

## 提交拆分（TDD）
1. `test(#1)`: 先提交失败测试（复现 1.005→100 症状 + 全部边界用例）
2. `feat(#1)`: 最小实现（Decimal + ROUND_HALF_UP）使测试转绿
