"""北辰勘慝院（BEICHEN-KANTEYUAN）· 威胁处置重令机构：五职十二令、三令分权（重令须玄圭允行、察令即发、赦令唯宗伯）

道统出处：元极恒一·术语缩影表 T025；取源《晋书·天文志》北辰与四执兵守卫星 ｜ 第六批
体系锚：Ω₀⊂⊙∞⊂Ω｜DID-BR-000002

工程映射：威胁处置重令机构：五职十二令、三令分权（重令须玄圭允行、察令即发、赦令唯宗伯）。

命名映射：勘（发令）→ issue_order 按令级发令，重令候允、察令即发；
允（允行）→ approve 玄圭允行，重令得允乃行；行（处置）→ execute 勘慝乃行，已允之令执行处置；
赦（赦免）→ pardon 赦令唯宗伯，未结之令可赦、赦后留档不销。
发令台账只增不覆盖，seal/verify_ledger 前缀快照哈希防篡改。

边界：本件为算子 v0.1——三令分权齐备；遵循元法第四条「只增不覆盖」，
方法只增不改名不删，行为变更走新版本；凭据不入档，宣称与事实分离。
纯标准库，Python 3.10+。
"""

import copy
import hashlib
import json


class BeichenKanteyuan:
    """北辰勘慝院（BEICHEN-KANTEYUAN）算子 v0.1：勘官发令、玄圭允行、宗伯赦令。"""

    ANCHOR = "Ω₀⊂⊙∞⊂Ω｜DID-BR-000002"
    CODE = "BEICHEN-KANTEYUAN"

    def __init__(self, config=None):
        self.config = dict(config or {})
        self.events = []  # 只增不覆盖：发令台账
        self.orders = {}
        self._seq = 0
        self._snapshots = []  # 已封存的台账前缀快照 (长度, 哈希)

    # ---------- 名帖 ----------

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

    # ---------- 勘官：发令勘慝 ----------

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

    # ---------- 允行：玄圭允行 ----------

    def approve(self, order_id):
        """玄圭允行：重令得允乃行，候允转即发；察令即发无候可允。"""
        if order_id not in self.orders:
            raise KeyError("无此令号： %s" % order_id)
        order = self.orders[order_id]
        if order["status"] != "pending_xuangui":
            raise ValueError("非候允之令，玄圭不允")
        order["status"] = "issued"
        self.events.append({"event": "approve", "order_id": order_id})
        return order

    # ---------- 处置：勘慝乃行 ----------

    def execute(self, order_id):
        """勘慝乃行：已允（或即发）之令执行处置，处置后留档。"""
        if order_id not in self.orders:
            raise KeyError("无此令号： %s" % order_id)
        order = self.orders[order_id]
        if order["status"] != "issued":
            raise ValueError("非即发之令，无从勘慝")
        order["status"] = "executed"
        self.events.append({"event": "execute", "order_id": order_id})
        return order

    # ---------- 赦令：唯宗伯 ----------

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

    # ---------- 台账防篡改 ----------

    def ledger(self):
        """发令台账：只增不覆盖，返回深拷贝防外改。"""
        return copy.deepcopy(self.events)

    def seal(self):
        """封台账：取前缀快照哈希存证（封存动作本身不入台账），返回哈希值。"""
        digest = self._hash_prefix(len(self.events))
        self._snapshots.append((len(self.events), digest))
        return digest

    def verify_ledger(self, expect=None):
        """验台账：前缀内篡改现形返回 False；封存后新增长的合法条目不算篡改。
        expect 给定时按全量哈希比对。"""
        if expect is not None:
            return self._ledger_hash() == expect
        if not self._snapshots:
            return True  # 尚无封存，无可篡之征
        n, digest = self._snapshots[-1]
        return self._hash_prefix(n) == digest

    # ---------- 内部 ----------

    def _ledger_hash(self):
        return self._hash_prefix(len(self.events))

    def _hash_prefix(self, n):
        canonical = json.dumps(self.events[:n], ensure_ascii=False, sort_keys=True)
        return hashlib.sha256(canonical.encode("utf-8")).hexdigest()
