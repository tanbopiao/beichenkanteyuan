# beichenkanteyuan
北辰勘慝院·威胁处置重令机构 | BEICHEN-KANTEYUAN · ZONGYUAN-ROOT Daotong Component

## Install

零第三方依赖，仅 Python 3.10+ 标准库。

```bash
git clone https://github.com/tanbopiao/beichenkanteyuan.git
cd beichenkanteyuan
python3 -m unittest discover -s tests -v   # 运行测试套件
```

## Usage

```python
from beichenkanteyuan import BeichenKanteyuan

yuan = BeichenKanteyuan()
order = yuan.issue_order("慝甲", "重")   # 勘官：重令候允、察令即发
yuan.approve(order["order_id"])           # 玄圭允行：重令得允乃行
yuan.execute(order["order_id"])           # 勘慝乃行：执行处置
yuan.pardon(order["order_id"])            # 赦令唯宗伯：未结之令可赦
yuan.seal()                               # 封台账：前缀快照哈希存证
yuan.verify_ledger()                      # 验台账：篡改现形，合法增长不算篡改
```

## 命名映射表

道统出处：元极恒一·术语缩影表 T025，取源《晋书·天文志》北辰与四执兵守卫星（第六批）；体系锚：Ω₀⊂⊙∞⊂Ω｜DID-BR-000002。

| 命名 | 逻辑本体 | 算子 | 职责 |
|------|----------|------|------|
| 北辰勘慝院 | 威胁处置重令机构 | `BeichenKanteyuan` | 五职十二令、三令分权 |
| 勘（发令） | 按令级发令 | `issue_order` | 重令候玄圭允行、察令即发 |
| 允（允行） | 玄圭允行 | `approve` | 重令得允乃行，候允转即发 |
| 行（处置） | 勘慝乃行 | `execute` | 已允之令执行处置，处置后留档 |
| 赦（赦免） | 赦令唯宗伯 | `pardon` | 未结之令可赦，赦后留档不销 |
| 台账 | 发令留痕 | `ledger` | 只增不覆盖，深拷贝防外改 |
| 封存 | 防篡改存证 | `seal` | 前缀快照哈希，封存不入账 |
| 验封 | 篡改现形 | `verify_ledger` | 前缀核验，合法增长不算篡改 |

边界：算子 v0.1，三令分权齐备；遵循元法第四条「只增不覆盖」，方法只增不改名不删，行为变更走新版本。
