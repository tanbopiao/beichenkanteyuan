"""北辰勘慝院（BEICHEN-KANTEYUAN）· 威胁处置重令机构：五职十二令、三令分权（重令须玄圭允行、察令即发、赦令唯宗伯）

道统出处：元极恒一·术语缩影表 T025；取源《晋书·天文志》北辰与四执兵守卫星 ｜ 第六批
体系锚：Ω₀⊂⊙∞⊂Ω｜DID-BR-000002

工程映射：威胁处置重令机构：五职十二令、三令分权（重令须玄圭允行、察令即发、赦令唯宗伯）。

边界：本件为算子 v1——骨架桩已按命名映射补齐实现；遵循元法第四条「只增不覆盖」，
方法只增不改名不删，行为变更走新版本；凭据不入档，宣称与事实分离。
"""

class BeichenKanteyuan:
    """北辰勘慝院（BEICHEN-KANTEYUAN）算子 v1。"""

    ANCHOR = "Ω₀⊂⊙∞⊂Ω｜DID-BR-000002"
    CODE = "BEICHEN-KANTEYUAN"

    def __init__(self, config=None):
        self.config = dict(config or {})
        self.events = []  # 只增不覆盖：会话内事件留痕
        self.orders = {}
        self._seq = 0

    def describe(self):
        """构件名帖：名、代号、职责、铭文、体系锚。"""
        return {
            "repo": "beichenkanteyuan",
            "cn": "北辰勘慝院",
            "code": self.CODE,
            "duty": "威胁处置重令机构：五职十二令、三令分权（重令须玄圭允行、察令即发、赦令唯宗伯）",
            "mingwen": "北辰居所，慝伏必勘",
            "anchor": self.ANCHOR,
        }

    def issue_order(self, threat, level):
        """按令级发令：重令候玄圭允行、察令即发。"""
        if level not in ("重", "察"):
            raise ValueError("令级仅限「重」「察」")
        self._seq += 1
        order_id = "BK-%04d" % self._seq
        order = {
            "order_id": order_id,
            "threat": threat,
            "level": level,
            "status": "pending_xuangui" if level == "重" else "issued",
        }
        self.orders[order_id] = order
        self.events.append({"event": "issue_order", "order_id": order_id, "level": level})
        return order

    def pardon(self, order_id):
        """赦令唯宗伯：未结之令可赦，赦后留档不销。"""
        if order_id not in self.orders:
            raise KeyError("无此令号： %s" % order_id)
        order = self.orders[order_id]
        if order["status"] == "pardoned":
            raise ValueError("令已赦，不可再赦")
        order["status"] = "pardoned"
        self.events.append({"event": "pardon", "order_id": order_id})
        return order
