# Spec: Issue #1 — 单价 1.005 元商品结算为 1.00 元

完整 Spec 见 Issue #1 评论（issue agent 已发布）。摘要：

## 目标
修正 `checkout.py::total_cents()` 的结算金额舍入逻辑：改用 `decimal.Decimal` 精确十进制运算并四舍五入到分（`ROUND_HALF_UP`），使 `total_cents("1.005", 1)` 返回 101（1.01 元）。

## 范围
- In：`checkout.py` 金额计算改 `Decimal` + `ROUND_HALF_UP`（字符串直构 `Decimal`，不经 `float` 中转）；补充单元测试。
- Out：不改签名/返回类型、不改调用方、不做展示格式化。

## 验收标准
- `total_cents("1.005", 1) == 101`；`("2.005", 1) == 201`；`("0.125", 1) == 13`
- 常规价格（"0.01"/"1.00"/"9.99"/"19.99"）与各数量结果与精确手算一致
- 签名与返回类型不变，实现中不再出现 `float(unit_price)`
- 全量现有测试通过，新增测试覆盖半分进位边界
